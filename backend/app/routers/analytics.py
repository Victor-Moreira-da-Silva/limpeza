from fastapi import APIRouter,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.deps import current_user
from app.models import *
from app.services.calculations import calculate_dilution,waste,required_staff,criticality_score
from app.schemas import DilutionCalcIn
router=APIRouter(tags=['analytics'])
@router.get('/dashboard')
def dashboard(db:Session=Depends(get_db),user=Depends(current_user),unit_id:int|None=None,sector_id:int|None=None):
    f=[Cost.tenant_id==user.tenant_id]; cf=[Consumption.tenant_id==user.tenant_id];
    if unit_id: f.append(Cost.unit_id==unit_id); cf.append(Consumption.unit_id==unit_id)
    if sector_id: f.append(Cost.sector_id==sector_id); cf.append(Consumption.sector_id==sector_id)
    total=float(db.query(func.coalesce(func.sum(Cost.amount),0)).filter(*f).scalar()); cons=float(db.query(func.coalesce(func.sum(Consumption.cost),0)).filter(*cf).scalar())
    tasks=db.query(Task).filter(Task.tenant_id==user.tenant_id); done=tasks.filter(Task.status=='concluída').count(); all_tasks=tasks.count() or 1
    ot=float(db.query(func.coalesce(func.sum(Employee.overtime_hours),0)).filter(Employee.tenant_id==user.tenant_id).scalar()); absences=db.query(func.coalesce(func.sum(Employee.absences),0)).filter(Employee.tenant_id==user.tenant_id).scalar() or 0
    nc=db.query(NonConformity).filter(NonConformity.tenant_id==user.tenant_id,NonConformity.status=='aberta').count()
    sectors=[]
    for s in db.query(Sector).filter(Sector.tenant_id==user.tenant_id).all():
        c=float(db.query(func.coalesce(func.sum(Cost.amount),0)).filter(Cost.tenant_id==user.tenant_id,Cost.sector_id==s.id).scalar()); co=float(db.query(func.coalesce(func.sum(Consumption.cost),0)).filter(Consumption.tenant_id==user.tenant_id,Consumption.sector_id==s.id).scalar())
        score=criticality_score(0 if not s.cost_goal else max((c-float(s.cost_goal))/float(s.cost_goal)*100,0),20 if co>0 else 0,85,95,0,nc)
        sectors.append({'id':s.id,'name':s.name,'score':score,'level':'CRÍTICO' if score>=70 else 'ATENÇÃO' if score>=40 else 'NORMAL','cost':c,'consumption':co})
    return {'cards':{'monthly_cost':total,'accumulated_cost':total,'budget':float(db.query(func.coalesce(func.sum(Unit.budget),0)).filter(Unit.tenant_id==user.tenant_id).scalar()),'consumption':cons,'waste':sum(max(float(x.quantity)-float(x.planned_quantity),0)*float(x.cost/max(float(x.quantity),1)) for x in db.query(Consumption).filter(*cf)),'productivity':round(done/all_tasks*100,2),'overtime_hours':ot,'absenteeism':absences,'non_conformities':nc,'critical_sectors':len([s for s in sectors if s['score']>=70])},'critical_sectors':sorted(sectors,key=lambda x:x['score'],reverse=True)}
@router.post('/dilutions/calculate')
def dilution_calc(payload:DilutionCalcIn,user=Depends(current_user)): return calculate_dilution(payload.volume_liters,payload.ratio,payload.product_price_per_liter)
@router.get('/dimensioning')
def dimensioning(area_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    a=db.query(Area).filter(Area.tenant_id==user.tenant_id,Area.id==area_id).first(); needed=required_staff(float(a.square_meters),a.criticality,1,20,1); scaled=db.query(Schedule).filter(Schedule.tenant_id==user.tenant_id,Schedule.area_id==area_id).count(); return {'area_id':area_id,'needed':needed,'scheduled':scaled,'delta':scaled-needed,'status':'excesso' if scaled>needed else 'déficit' if scaled<needed else 'adequado'}
@router.get('/reports/{kind}')
def report(kind:str,db:Session=Depends(get_db),user=Depends(current_user),format:str='json'):
    data={'custos':db.query(Cost).filter(Cost.tenant_id==user.tenant_id).all(),'consumo':db.query(Consumption).filter(Consumption.tenant_id==user.tenant_id).all(),'estoque':db.query(Stock).filter(Stock.tenant_id==user.tenant_id).all()}.get(kind,[])
    if format=='csv': return {'filename':f'{kind}.csv','rows':[getattr(x,'id',None) for x in data]}
    return data
@router.get('/audit')
def audit(db:Session=Depends(get_db),user=Depends(current_user)): return db.query(AuditLog).filter(AuditLog.tenant_id==user.tenant_id).order_by(AuditLog.id.desc()).limit(200).all()

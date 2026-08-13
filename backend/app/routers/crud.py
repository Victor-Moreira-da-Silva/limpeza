from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.deps import current_user,require
from app import models,schemas
router=APIRouter()
MAP={'tenants':(models.Tenant,schemas.TenantIn,'admin:write'),'units':(models.Unit,schemas.UnitIn,'admin:write'),'sectors':(models.Sector,schemas.SectorIn,'operation:write'),'areas':(models.Area,schemas.AreaIn,'operation:write'),'employees':(models.Employee,schemas.EmployeeIn,'people:write'),'products':(models.Product,schemas.ProductIn,'materials:write'),'consumption':(models.Consumption,schemas.ConsumptionIn,'materials:write'),'schedules':(models.Schedule,schemas.ScheduleIn,'people:write'),'tasks':(models.Task,schemas.TaskIn,'operation:write'),'laundry':(models.LaundryBatch,schemas.LaundryBatchIn,'laundry:write'),'costs':(models.Cost,schemas.CostIn,'management:write'),'goals':(models.Goal,schemas.GoalIn,'management:write')}
def tenant_filter(q,model,user):
    return q.filter(model.tenant_id==user.tenant_id) if hasattr(model,'tenant_id') else q
@router.get('/{resource}')
def list_items(resource:str,db:Session=Depends(get_db),user=Depends(current_user),unit_id:int|None=None,sector_id:int|None=None,area_id:int|None=None):
    if resource not in MAP: raise HTTPException(404,'recurso inválido')
    model,_,_=MAP[resource]; q=tenant_filter(db.query(model),model,user)
    for k,v in {'unit_id':unit_id,'sector_id':sector_id,'area_id':area_id}.items():
        if v is not None and hasattr(model,k): q=q.filter(getattr(model,k)==v)
    return q.limit(500).all()
@router.post('/{resource}')
def create_item(resource:str,payload:dict,db:Session=Depends(get_db),user=Depends(current_user)):
    if resource not in MAP: raise HTTPException(404,'recurso inválido')
    model,schema,perm=MAP[resource]; require(perm)(user,db); data=schema(**payload).model_dump(); obj=model(**data)
    if hasattr(model,'tenant_id'): obj.tenant_id=user.tenant_id
    db.add(obj); db.flush(); db.add(models.AuditLog(tenant_id=user.tenant_id,user_id=user.id,entity=resource,entity_id=obj.id,action='create',new_value=str(data))); db.commit(); db.refresh(obj); return obj
@router.put('/{resource}/{item_id}')
def update_item(resource:str,item_id:int,payload:dict,db:Session=Depends(get_db),user=Depends(current_user)):
    if resource not in MAP: raise HTTPException(404,'recurso inválido')
    model,schema,perm=MAP[resource]; require(perm)(user,db); obj=tenant_filter(db.query(model),model,user).filter(model.id==item_id).first()
    if not obj: raise HTTPException(404,'não encontrado')
    old=str({c.name:getattr(obj,c.name) for c in model.__table__.columns}); data=schema(**payload).model_dump()
    for k,v in data.items(): setattr(obj,k,v)
    db.add(models.AuditLog(tenant_id=user.tenant_id,user_id=user.id,entity=resource,entity_id=item_id,action='update',old_value=old,new_value=str(data))); db.commit(); return obj
@router.delete('/{resource}/{item_id}')
def delete_item(resource:str,item_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    if resource not in MAP: raise HTTPException(404,'recurso inválido')
    model,_,perm=MAP[resource]; require(perm)(user,db); obj=tenant_filter(db.query(model),model,user).filter(model.id==item_id).first()
    if not obj: raise HTTPException(404,'não encontrado')
    db.delete(obj); db.add(models.AuditLog(tenant_id=user.tenant_id,user_id=user.id,entity=resource,entity_id=item_id,action='delete')); db.commit(); return {'deleted':True}

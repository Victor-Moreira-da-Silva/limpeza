from datetime import date,time
from app.db.session import Base,engine,SessionLocal
from app.models import *
from app.services.security import hash_password
ROLES=['Administrador','Diretor','Gerente','Coordenador','Supervisor','Líder','Almoxarifado','Lavanderia','Colaborador','Auditor']
PERMS=['admin:write','operation:write','people:write','materials:write','laundry:write','management:write','reports:read','audit:read']
def run():
    Base.metadata.create_all(engine); db=SessionLocal()
    if db.query(Tenant).first(): return
    t=Tenant(name='Empresa Demonstração Limpeza360',cnpj='00.000.000/0001-00'); db.add(t); db.flush()
    roles={r:Role(name=r,description=r) for r in ROLES}; perms={p:Permission(code=p,description=p) for p in PERMS}; db.add_all([*roles.values(),*perms.values()]); db.flush()
    roles['Administrador'].permissions=list(perms.values()) if hasattr(roles['Administrador'],'permissions') else []
    admin=User(tenant_id=t.id,email='admin@limpeza360.local',password_hash=hash_password('Admin123!'),full_name='Administrador Desenvolvimento',role_id=roles['Administrador'].id)
    u=Unit(tenant_id=t.id,name='Hospital Central',code='HC',budget=650000); db.add_all([admin,u]); db.flush()
    s=Sector(tenant_id=t.id,unit_id=u.id,name='UTI',code='UTI',responsible='Maria Gestora',square_meters=680,classification='crítica',criticality=92,cost_goal=90000,cleaning_frequency='3x ao dia')
    db.add(s); db.flush(); a=Area(tenant_id=t.id,sector_id=s.id,name='UTI Adulto',square_meters=420,type='assistencial',criticality=95,frequency='3x ao dia',required_staff=8); db.add(a); db.flush()
    e=Employee(tenant_id=t.id,name='João Silva',registration='MAT-001',role_name='Auxiliar de limpeza',sector_id=s.id,area_id=a.id,shift='Manhã',journey='12x36',salary_cost=4200,productivity=91,overtime_hours=12)
    cat=Category(tenant_id=t.id,name='Químicos',type='produto'); sup=Supplier(tenant_id=t.id,name='Fornecedor Pro',cnpj='11.111.111/0001-11',rating=4.7); db.add_all([e,cat,sup]); db.flush()
    p=Product(tenant_id=t.id,category_id=cat.id,supplier_id=sup.id,name='Desinfetante X',unit='L',concentration='concentrado',price=38,min_stock=20,max_stock=120); db.add(p); db.flush()
    db.add_all([Stock(tenant_id=t.id,product_id=p.id,unit_id=u.id,quantity=18),Consumption(tenant_id=t.id,product_id=p.id,unit_id=u.id,sector_id=s.id,area_id=a.id,employee_id=e.id,date=date.today(),shift='Manhã',planned_quantity=100,quantity=130,cost=4940),Cost(tenant_id=t.id,unit_id=u.id,sector_id=s.id,area_id=a.id,employee_id=e.id,type='materiais',amount=4940,date=date.today()),LaundryBatch(tenant_id=t.id,unit_id=u.id,sector_id=s.id,code='LAV-001',status='lavagem',kg_received=320,kg_processed=280,cost=2100),Task(tenant_id=t.id,area_id=a.id,responsible_id=e.id,type='desinfecção',priority='alta',status='pendente'),NonConformity(tenant_id=t.id,sector_id=s.id,severity='crítica',description='Checklist com item não conforme')])
    db.commit(); print('Seed concluído. Login: admin@limpeza360.local / Admin123!')
if __name__=='__main__': run()

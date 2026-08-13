from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.session import Base
class TenantScoped:
    tenant_id=Column(ForeignKey('tenants.id'),nullable=False,index=True)
class Tenant(Base):
    __tablename__='tenants'; id=Column(Integer,primary_key=True); name=Column(String(160),nullable=False); cnpj=Column(String(20)); active=Column(Boolean,default=True)
class Role(Base):
    __tablename__='roles'; id=Column(Integer,primary_key=True); name=Column(String(60),unique=True); description=Column(String(200)); permissions=relationship('Permission',secondary=lambda: role_permissions)
class Permission(Base):
    __tablename__='permissions'; id=Column(Integer,primary_key=True); code=Column(String(80),unique=True); description=Column(String(200))
role_permissions=Table('role_permissions',Base.metadata,Column('role_id',ForeignKey('roles.id'),primary_key=True),Column('permission_id',ForeignKey('permissions.id'),primary_key=True))
class User(Base,TenantScoped):
    __tablename__='users'; id=Column(Integer,primary_key=True); email=Column(String(180),unique=True,index=True); password_hash=Column(String(255)); full_name=Column(String(160)); active=Column(Boolean,default=True); mfa_enabled=Column(Boolean,default=False); role_id=Column(ForeignKey('roles.id')); role=relationship('Role')
class Unit(Base,TenantScoped):
    __tablename__='units'; id=Column(Integer,primary_key=True); name=Column(String(160)); code=Column(String(30)); budget=Column(Numeric(14,2),default=0)
class Sector(Base,TenantScoped):
    __tablename__='sectors'; id=Column(Integer,primary_key=True); unit_id=Column(ForeignKey('units.id')); name=Column(String(160)); code=Column(String(30)); responsible=Column(String(120)); square_meters=Column(Numeric(12,2),default=0); classification=Column(String(40)); criticality=Column(Integer,default=0); cost_goal=Column(Numeric(14,2),default=0); cleaning_frequency=Column(String(80))
class Area(Base,TenantScoped):
    __tablename__='areas'; id=Column(Integer,primary_key=True); sector_id=Column(ForeignKey('sectors.id')); name=Column(String(160)); square_meters=Column(Numeric(12,2),default=0); type=Column(String(80)); criticality=Column(Integer,default=0); frequency=Column(String(80)); required_staff=Column(Integer,default=1)
class Environment(Base,TenantScoped):
    __tablename__='environments'; id=Column(Integer,primary_key=True); area_id=Column(ForeignKey('areas.id')); name=Column(String(120)); beds=Column(Integer,default=0); rooms=Column(Integer,default=0); bathrooms=Column(Integer,default=0); risk_level=Column(String(40))
class Employee(Base,TenantScoped):
    __tablename__='employees'; id=Column(Integer,primary_key=True); name=Column(String(160)); registration=Column(String(40)); role_name=Column(String(80)); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); shift=Column(String(40)); journey=Column(String(40)); salary_cost=Column(Numeric(14,2),default=0); status=Column(String(30),default='ativo'); productivity=Column(Numeric(5,2),default=0); absences=Column(Integer,default=0); delays=Column(Integer,default=0); overtime_hours=Column(Numeric(8,2),default=0)
class Schedule(Base,TenantScoped):
    __tablename__='schedules'; id=Column(Integer,primary_key=True); employee_id=Column(ForeignKey('employees.id')); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); date=Column(Date); start_time=Column(Time); end_time=Column(Time); pattern=Column(String(30)); event_type=Column(String(30),default='plantao')
class Checklist(Base,TenantScoped):
    __tablename__='checklists'; id=Column(Integer,primary_key=True); area_id=Column(ForeignKey('areas.id')); name=Column(String(160)); active=Column(Boolean,default=True)
class ChecklistItem(Base,TenantScoped):
    __tablename__='checklist_items'; id=Column(Integer,primary_key=True); checklist_id=Column(ForeignKey('checklists.id')); label=Column(String(160)); status=Column(String(30),default='pendente'); observation=Column(Text); photo_url=Column(String(255)); signature=Column(String(255)); responsible_id=Column(ForeignKey('employees.id')); checked_at=Column(DateTime)
class Task(Base,TenantScoped):
    __tablename__='tasks'; id=Column(Integer,primary_key=True); area_id=Column(ForeignKey('areas.id')); responsible_id=Column(ForeignKey('employees.id')); checklist_id=Column(ForeignKey('checklists.id')); type=Column(String(80)); due_at=Column(DateTime); estimated_minutes=Column(Integer); priority=Column(String(30)); status=Column(String(30),default='pendente')
class Supplier(Base,TenantScoped):
    __tablename__='suppliers'; id=Column(Integer,primary_key=True); name=Column(String(160)); cnpj=Column(String(20)); contact=Column(String(160)); delivery_days=Column(Integer); payment_terms=Column(String(120)); rating=Column(Numeric(3,2),default=0)
class Category(Base,TenantScoped):
    __tablename__='categories'; id=Column(Integer,primary_key=True); name=Column(String(100)); type=Column(String(40))
class Product(Base,TenantScoped):
    __tablename__='products'; id=Column(Integer,primary_key=True); category_id=Column(ForeignKey('categories.id')); supplier_id=Column(ForeignKey('suppliers.id')); name=Column(String(160)); manufacturer=Column(String(120)); unit=Column(String(20)); concentration=Column(String(40)); package=Column(String(80)); price=Column(Numeric(14,4),default=0); lot=Column(String(80)); expires_at=Column(Date); min_stock=Column(Numeric(14,3),default=0); max_stock=Column(Numeric(14,3),default=0)
class Stock(Base,TenantScoped):
    __tablename__='stock'; id=Column(Integer,primary_key=True); product_id=Column(ForeignKey('products.id')); unit_id=Column(ForeignKey('units.id')); quantity=Column(Numeric(14,3),default=0); lot=Column(String(80)); expires_at=Column(Date)
class StockMovement(Base,TenantScoped):
    __tablename__='stock_movements'; id=Column(Integer,primary_key=True); stock_id=Column(ForeignKey('stock.id')); type=Column(String(30)); quantity=Column(Numeric(14,3)); reason=Column(String(160)); created_at=Column(DateTime,server_default=func.now()); user_id=Column(ForeignKey('users.id'))
class Dilution(Base,TenantScoped):
    __tablename__='dilutions'; id=Column(Integer,primary_key=True); product_id=Column(ForeignKey('products.id')); ratio=Column(String(20)); original_concentration=Column(String(40)); recommended_concentration=Column(String(40)); method=Column(String(160))
class Consumption(Base,TenantScoped):
    __tablename__='consumption'; id=Column(Integer,primary_key=True); product_id=Column(ForeignKey('products.id')); unit_id=Column(ForeignKey('units.id')); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); employee_id=Column(ForeignKey('employees.id')); date=Column(Date); shift=Column(String(40)); planned_quantity=Column(Numeric(14,3),default=0); quantity=Column(Numeric(14,3),default=0); cost=Column(Numeric(14,2),default=0)
class PurchaseOrder(Base,TenantScoped):
    __tablename__='purchase_orders'; id=Column(Integer,primary_key=True); supplier_id=Column(ForeignKey('suppliers.id')); status=Column(String(40),default='solicitado'); requested_at=Column(DateTime,server_default=func.now()); approved_by=Column(ForeignKey('users.id')); total=Column(Numeric(14,2),default=0)
class PurchaseOrderItem(Base,TenantScoped):
    __tablename__='purchase_order_items'; id=Column(Integer,primary_key=True); order_id=Column(ForeignKey('purchase_orders.id')); product_id=Column(ForeignKey('products.id')); quantity=Column(Numeric(14,3)); unit_price=Column(Numeric(14,4))
class LaundryBatch(Base,TenantScoped):
    __tablename__='laundry_batches'; id=Column(Integer,primary_key=True); unit_id=Column(ForeignKey('units.id')); sector_id=Column(ForeignKey('sectors.id')); code=Column(String(80)); status=Column(String(40)); kg_received=Column(Numeric(14,3),default=0); kg_processed=Column(Numeric(14,3),default=0); kg_delivered=Column(Numeric(14,3),default=0); kg_lost=Column(Numeric(14,3),default=0); kg_discarded=Column(Numeric(14,3),default=0); cost=Column(Numeric(14,2),default=0)
class LaundryStep(Base,TenantScoped):
    __tablename__='laundry_steps'; id=Column(Integer,primary_key=True); batch_id=Column(ForeignKey('laundry_batches.id')); step=Column(String(40)); responsible_id=Column(ForeignKey('employees.id')); quantity=Column(Integer); weight_kg=Column(Numeric(14,3)); occurrence=Column(Text); created_at=Column(DateTime,server_default=func.now())
class Linen(Base,TenantScoped):
    __tablename__='linen'; id=Column(Integer,primary_key=True); type=Column(String(80)); status=Column(String(40)); quantity=Column(Integer); ideal_stock=Column(Integer); unit_id=Column(ForeignKey('units.id'))
class LinenMovement(Base,TenantScoped):
    __tablename__='linen_movements'; id=Column(Integer,primary_key=True); linen_id=Column(ForeignKey('linen.id')); origin=Column(String(120)); destination=Column(String(120)); quantity=Column(Integer); weight_kg=Column(Numeric(14,3)); responsible_id=Column(ForeignKey('employees.id')); created_at=Column(DateTime,server_default=func.now())
class Occurrence(Base,TenantScoped):
    __tablename__='occurrences'; id=Column(Integer,primary_key=True); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); severity=Column(String(30)); description=Column(Text); status=Column(String(30),default='aberta')
class NonConformity(Base,TenantScoped):
    __tablename__='non_conformities'; id=Column(Integer,primary_key=True); sector_id=Column(ForeignKey('sectors.id')); severity=Column(String(30)); description=Column(Text); status=Column(String(30),default='aberta')
class CostCenter(Base,TenantScoped):
    __tablename__='cost_centers'; id=Column(Integer,primary_key=True); name=Column(String(120)); budget=Column(Numeric(14,2),default=0)
class Cost(Base,TenantScoped):
    __tablename__='costs'; id=Column(Integer,primary_key=True); cost_center_id=Column(ForeignKey('cost_centers.id')); unit_id=Column(ForeignKey('units.id')); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); employee_id=Column(ForeignKey('employees.id')); type=Column(String(40)); amount=Column(Numeric(14,2)); date=Column(Date); description=Column(String(160))
class Goal(Base,TenantScoped):
    __tablename__='goals'; id=Column(Integer,primary_key=True); scope=Column(String(40)); unit_id=Column(ForeignKey('units.id')); sector_id=Column(ForeignKey('sectors.id')); area_id=Column(ForeignKey('areas.id')); metric=Column(String(80)); target=Column(Numeric(14,2)); period_start=Column(Date); period_end=Column(Date)
class Indicator(Base,TenantScoped):
    __tablename__='indicators'; id=Column(Integer,primary_key=True); metric=Column(String(80)); value=Column(Numeric(14,4)); scope=Column(String(40)); calculated_at=Column(DateTime,server_default=func.now())
class AuditLog(Base,TenantScoped):
    __tablename__='audit_logs'; id=Column(Integer,primary_key=True); user_id=Column(ForeignKey('users.id')); entity=Column(String(80)); entity_id=Column(Integer); action=Column(String(30)); old_value=Column(Text); new_value=Column(Text); created_at=Column(DateTime,server_default=func.now())
class Notification(Base,TenantScoped):
    __tablename__='notifications'; id=Column(Integer,primary_key=True); level=Column(String(20)); title=Column(String(160)); message=Column(Text); read=Column(Boolean,default=False); created_at=Column(DateTime,server_default=func.now())

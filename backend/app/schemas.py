from pydantic import BaseModel,EmailStr
from datetime import date,datetime,time
class LoginIn(BaseModel): email:EmailStr; password:str
class TokenOut(BaseModel): access_token:str; refresh_token:str; token_type:str='bearer'
class TenantIn(BaseModel): name:str; cnpj:str|None=None
class UnitIn(BaseModel): name:str; code:str|None=None; budget:float=0
class SectorIn(BaseModel): unit_id:int; name:str; code:str|None=None; responsible:str|None=None; square_meters:float=0; classification:str|None=None; criticality:int=0; cost_goal:float=0; cleaning_frequency:str|None=None
class AreaIn(BaseModel): sector_id:int; name:str; square_meters:float=0; type:str|None=None; criticality:int=0; frequency:str|None=None; required_staff:int=1
class EmployeeIn(BaseModel): name:str; registration:str; role_name:str|None=None; sector_id:int|None=None; area_id:int|None=None; shift:str|None=None; journey:str|None=None; salary_cost:float=0; status:str='ativo'
class ProductIn(BaseModel): name:str; category_id:int|None=None; supplier_id:int|None=None; manufacturer:str|None=None; unit:str='L'; concentration:str|None=None; package:str|None=None; price:float=0; lot:str|None=None; expires_at:date|None=None; min_stock:float=0; max_stock:float=0
class ConsumptionIn(BaseModel): product_id:int; unit_id:int; sector_id:int|None=None; area_id:int|None=None; employee_id:int|None=None; date:date; shift:str|None=None; planned_quantity:float=0; quantity:float; cost:float=0
class StockMoveIn(BaseModel): stock_id:int; type:str; quantity:float; reason:str|None=None
class DilutionCalcIn(BaseModel): volume_liters:float; ratio:str; product_price_per_liter:float
class ScheduleIn(BaseModel): employee_id:int; sector_id:int|None=None; area_id:int|None=None; date:date; start_time:time; end_time:time; pattern:str; event_type:str='plantao'
class TaskIn(BaseModel): area_id:int; responsible_id:int|None=None; checklist_id:int|None=None; type:str; due_at:datetime|None=None; estimated_minutes:int=0; priority:str='normal'; status:str='pendente'
class LaundryBatchIn(BaseModel): unit_id:int; sector_id:int|None=None; code:str; status:str='recebimento'; kg_received:float=0; kg_processed:float=0; kg_delivered:float=0; kg_lost:float=0; kg_discarded:float=0; cost:float=0
class CostIn(BaseModel): cost_center_id:int|None=None; unit_id:int|None=None; sector_id:int|None=None; area_id:int|None=None; employee_id:int|None=None; type:str; amount:float; date:date; description:str|None=None
class GoalIn(BaseModel): scope:str; metric:str; target:float; unit_id:int|None=None; sector_id:int|None=None; area_id:int|None=None; period_start:date; period_end:date

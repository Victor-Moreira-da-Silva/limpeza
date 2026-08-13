from math import ceil
def calculate_dilution(volume_liters:float, ratio:str, product_price_per_liter:float):
    left,right=[float(x) for x in ratio.split(':')]; product_l=volume_liters*(left/right); water_l=max(volume_liters-product_l,0); cost=product_l*product_price_per_liter
    return {'product_ml':round(product_l*1000,3),'water_ml':round(water_l*1000,3),'final_volume_l':volume_liters,'solution_cost':round(cost,2),'cost_per_liter':round(cost/volume_liters,2) if volume_liters else 0}
def waste(planned,real,unit_cost):
    excess=max(real-planned,0); deviation=((real-planned)/planned*100) if planned else 0
    return {'deviation_percent':round(deviation,2),'waste_quantity':excess,'excess_cost':round(excess*unit_cost,2),'alert':deviation>=20}
def required_staff(square_meters,criticality,frequency_per_day,estimated_minutes=20,environments=1):
    factor=1+(criticality/100); workload=(square_meters/250)*factor*frequency_per_day+(estimated_minutes*environments/480)
    return max(1,ceil(workload))
def criticality_score(cost_dev,waste_dev,productivity,coverage,occurrences,non_conformities):
    score=cost_dev*.2+waste_dev*.25+(100-productivity)*.2+(100-coverage)*.15+min(occurrences*4,10)+min(non_conformities*5,10)
    return max(0,min(100,round(score,1)))

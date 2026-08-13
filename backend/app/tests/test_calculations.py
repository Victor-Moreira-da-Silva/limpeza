from app.services.calculations import calculate_dilution,waste,required_staff,criticality_score
def test_dilution_1_to_100():
    r=calculate_dilution(10,'1:100',38)
    assert r['product_ml']==100
    assert r['water_ml']==9900
    assert r['solution_cost']==3.8
def test_waste_alert():
    r=waste(100,130,5)
    assert r['deviation_percent']==30
    assert r['excess_cost']==150
    assert r['alert'] is True
def test_dimensioning_and_criticality():
    assert required_staff(680,95,3)>=8
    assert criticality_score(30,28,70,80,3,2)>30

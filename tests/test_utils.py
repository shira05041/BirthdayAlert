from website.utils import calculate_age
from datetime import date

def test_calculate_age():
    birth_date = date(2000,1,1)
    expected_age = date.today().year - 2000
    assert calculate_age(birth_date) == expected_age
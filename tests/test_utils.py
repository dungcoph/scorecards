from src.utils import *


def test_convert_date_to_years():
    assert convert_date_to_years('2023-09-01T00:00:00') == 0
    assert convert_date_to_years('2023-02-01T00:00:00') == 0
    assert convert_date_to_years('2022-12-01T00:00:00') == 0
    assert convert_date_to_years('2022-09-01T00:00:00') == 1
    assert convert_date_to_years('2022-01-01T00:00:00') == 1
    assert convert_date_to_years('2020-04-01T00:00:00') == 3


def test_get_number_or_inf_from_string():
    assert get_number_from_string('PD = exp(0.27882 - 0.014802 * score_sum)') == [0.27882, 0.014802]
    assert get_number_from_string('4|5|6') == [4, 5, 6]
    assert get_number_from_string('4') == [4]
    assert get_number_from_string('(0,2]') == [0, 2]
    assert get_number_from_string('(-inf,0]') == [-math.inf, 0]
    assert get_number_from_string('(2000,inf]') == [2000, math.inf]

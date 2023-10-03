from src.application import *
from tests.sample_data import get_sample_data


application = get_sample_data('CC_00.json')
application_with_null = get_sample_data('CC_null.json')


def test_input():
    input_data = application.input

    assert input_data.product_type == 'CC'
    assert input_data.application_date == "2023-09-15T14:14:51.229139"
    assert input_data.car_loan_debt == 28000
    assert input_data.mortgage_debt == 0
    assert input_data.study_loan_debt == 7000
    assert input_data.unsecured_debt == 36000
    assert input_data.requested_loan_amount is None


def test_applicant():
    applicant = application.input.applicant1
    applicant_with_null = application_with_null.input.applicant1

    assert applicant.age == 48
    assert applicant.accomodation_type_id == 2
    assert applicant.employment_type_id == 2
    assert applicant.gross_yearly_income == 24000
    assert applicant.monthly_rent == 1600
    assert applicant.employed_since == "2023-02-01T00:00:00"

    assert applicant_with_null.accomodation_type_id is None
    assert applicant_with_null.gross_yearly_income is None
    assert applicant_with_null.employed_since is None


def test_input_data():
    input_data = build_input_data(application)

    assert input_data.accomodation_type_id == 2
    assert input_data.employment_type_id == 2
    assert input_data.gross_yearly_income == 24000
    assert input_data.unsecured_debt == 36000
    assert input_data.years_employed_at_current_job == 0


from dataclasses import dataclass, field
from src.utils import convert_date_to_years


@dataclass
class Applicant:
    age: int
    accomodation_type_id: int
    employment_type_id: int
    gross_yearly_income: int
    monthly_rent: int
    employed_since: str


@dataclass
class Input:
    product_type: str
    application_date: str
    car_loan_debt: int
    mortgage_debt: int
    study_loan_debt: int
    unsecured_debt: int
    requested_loan_amount: int
    applicant1: Applicant


@dataclass
class Output:
    score_sum: float
    pd: float
    scorecard_name: str


@dataclass
class Application:
    input: Input
    output: Output


@dataclass
class InputData:
    product_type: str
    unsecured_debt: int
    accomodation_type_id: int
    employment_type_id: int
    gross_yearly_income: int
    years_employed_at_current_job: str
    _years_employed_at_current_job: int = field(init=False, repr=False)

    @property
    def years_employed_at_current_job(self) -> int:
        return self._years_employed_at_current_job

    @years_employed_at_current_job.setter
    def years_employed_at_current_job(self, employed_since: str):
        self._years_employed_at_current_job = convert_date_to_years(employed_since)


def build_input_data(application: Application):
    applicant = application.input.applicant1
    return InputData(application.input.product_type,
                     application.input.unsecured_debt,
                     applicant.accomodation_type_id,
                     applicant.employment_type_id,
                     applicant.gross_yearly_income,
                     applicant.employed_since)


from dataclasses import dataclass
from enum import Enum


@dataclass
class BandPoint:
    band: list[float]
    point: float


class VariableType(Enum):
    CATEGORY = 1
    RANGE = 2


@dataclass
class Variable:
    name: str
    type: VariableType


@dataclass
class ScorecardVariable:
    variable: Variable
    scores: list[BandPoint]
    missing: float


@dataclass
class Scorecard:
    scorecard_list: list[ScorecardVariable]
    calibration_equation: list[float]
    intercept: float
    name: str


VARIABLES_MAPPING = {
    'AccomodationTypeID': Variable('accomodation_type_id', VariableType.CATEGORY),
    'EmploymentTypeID': Variable('employment_type_id', VariableType.CATEGORY),
    'YearsEmployedAtCurrentJob': Variable('years_employed_at_current_job', VariableType.RANGE),
    'GrossYearlyIncome': Variable('gross_yearly_income', VariableType.RANGE),
    'UnsecuredDebt': Variable('unsecured_debt', VariableType.RANGE)
}

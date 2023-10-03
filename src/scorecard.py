from typing import Union
import math
from src.variables import Scorecard, ScorecardVariable, VariableType, BandPoint
from src.application import InputData, Output


def score_sum(scorecard_list: list[ScorecardVariable], intercept: float, input_data: InputData) -> float:
    sum_score = intercept

    # Loop through all scorecard of each variable
    for scorecard_variable in scorecard_list:
        # Get variable that apply for this scores
        variable = scorecard_variable.variable

        # Get variable data from input data
        variable_input = getattr(input_data, variable.name, None)

        # Check type of variable to use correct funtion to calculate score for this variable
        if variable.type == VariableType.CATEGORY:
            sum_score += category_type_score(scorecard_variable.scores, scorecard_variable.missing, variable_input)
        elif variable.type == VariableType.RANGE:
            sum_score += range_type_score(scorecard_variable.scores, scorecard_variable.missing, variable_input)
    return sum_score


def category_type_score(list_band_point: list[BandPoint], missing: float, data: Union[int, None]) -> float:
    # Calculate score for category type variable
    if data is None:
        # If the input data is missing return missing point
        return missing
    else:
        # If the input data is not missing, looking up value of input in all bands to find correct point
        for band_point in list_band_point:
            if data in band_point.band:
                return band_point.point


def range_type_score(list_band_point: list[BandPoint], missing: float, data: Union[int, None]) -> float:
    # Calculate score for range type variable
    if data is None:
        # If the input data is missing return missing point
        return missing
    for band_point in list_band_point:
        # If the input data is not missing, compare the data input with range to get correct point
        if band_point.band[0] < data <= band_point.band[1]:
            return band_point.point


def probability_of_default(k1: float, k2: float, score: float) -> float:
    # Calculate probability of default from score and 2 constants
    pd = math.exp(k1 - k2 * score)
    if pd > 1:
        pd = 1
    return pd


def calculate_scorecard(scorecard: Scorecard, input_data: InputData) -> Output:
    score = score_sum(scorecard.scorecard_list, scorecard.intercept, input_data)
    pd = probability_of_default(scorecard.calibration_equation[0], scorecard.calibration_equation[1], score)
    return Output(score, pd, scorecard.name)

from src.application import build_input_data
from src.scorecard import *
from src.variables import Variable, VariableType
from tests.sample_data import get_sample_data

score_card = Scorecard(
    [
        ScorecardVariable(
            Variable('accomodation_type_id', VariableType.CATEGORY),
            [BandPoint([1.0], 33.0),
             BandPoint([2.0, 3.0], -10.0),
             BandPoint([4.0], 0.0)],
            0.0
        ),
        ScorecardVariable(
            Variable('employment_type_id', VariableType.CATEGORY),
            [BandPoint([1.0], 40.0),
             BandPoint([2.0], 0.0),
             BandPoint([3.0], -10.0),
             BandPoint([5.0], 23.0),
             BandPoint([4.0, 6.0, 7.0], 0.0)],
            0.0
        ),
        ScorecardVariable(
            Variable('years_employed_at_current_job', VariableType.RANGE),
            [BandPoint([-math.inf, 0.0], -40.0),
             BandPoint([0.0, 2.0], 0.0),
             BandPoint([2.0, math.inf], 36.0)],
            0.0
        ),
        ScorecardVariable(
            Variable('gross_yearly_income', VariableType.RANGE),
            [BandPoint([-math.inf, 20300.0], -22.0),
             BandPoint([20300.0, 35000.0], -3.0),
             BandPoint([35000.0, math.inf], 0.0)],
            0.0
        )
    ],
    [0.27882, 0.014802],
    203.0,
    'CC'
)
cc_00_application = get_sample_data('CC_00.json')


def test_category_type_score():
    # Test category_type_score with bands:
    # [BandPoint([1.0], 33.0),
    #  BandPoint([2.0, 3.0], -10.0),
    #  BandPoint([4.0], 0.0)]
    category_scores = score_card.scorecard_list[0].scores
    assert category_type_score(category_scores, 0, 1) == 33
    assert category_type_score(category_scores, 0, 2) == -10
    assert category_type_score(category_scores, 0, 3) == -10
    assert category_type_score(category_scores, 0, 4) == 0
    assert category_type_score(category_scores, 0, None) == 0
    assert category_type_score(category_scores, 200, None) == 200


def test_range_type_score():
    # Test range_type_score with bands:
    # [BandPoint([-math.inf, 20300.0], -22.0),
    #  BandPoint([20300.0, 35000.0], -3.0),
    #  BandPoint([35000.0, math.inf], 0.0)]

    range_scores = score_card.scorecard_list[3].scores
    assert range_type_score(range_scores, 0, -1) == -22
    assert range_type_score(range_scores, 0, 20300) == -22
    assert range_type_score(range_scores, 0, 25000) == -3
    assert range_type_score(range_scores, 0, 35000) == -3
    assert range_type_score(range_scores, 0, 35001) == 0
    assert range_type_score(range_scores, 0, 40000) == 0
    assert range_type_score(range_scores, 0, None) == 0
    assert range_type_score(range_scores, 20, None) == 20


def test_score_sum():
    # Test score sum for application CC_00
    # "accomodation_type_id": 2,
    # "employment_type_id": 2,
    # "gross_yearly_income": 24000,
    # "employed_since": "2023-02-01T00:00:00" -> years_employed_at_current_job = 0
    # score_sum = 203 - 10 + 0 - 40 - 3 = 150
    input_data = build_input_data(cc_00_application)

    assert category_type_score(score_card.scorecard_list[0].scores,
                               score_card.scorecard_list[0].missing,
                               input_data.accomodation_type_id) == -10
    assert category_type_score(score_card.scorecard_list[1].scores,
                               score_card.scorecard_list[1].missing,
                               input_data.employment_type_id) == 0
    assert range_type_score(score_card.scorecard_list[2].scores,
                            score_card.scorecard_list[2].missing,
                            input_data.years_employed_at_current_job) == -40
    assert range_type_score(score_card.scorecard_list[3].scores,
                            score_card.scorecard_list[3].missing,
                            input_data.gross_yearly_income) == -3
    assert score_sum(score_card.scorecard_list, score_card.intercept, input_data) == 150


def test_score_sum_with_missing_data():
    # Test score sum for application CC_null
    # "accomodation_type_id": null,
    # "employment_type_id": 2,
    # "gross_yearly_income": null,
    # "employed_since": null
    # score_sum = 203 + 0 + 0 + 0 + 0 = 203
    cc_null_application = get_sample_data('CC_null.json')
    input_data = build_input_data(cc_null_application)

    assert category_type_score(score_card.scorecard_list[0].scores,
                               score_card.scorecard_list[0].missing,
                               input_data.accomodation_type_id) == 0
    assert category_type_score(score_card.scorecard_list[1].scores,
                               score_card.scorecard_list[1].missing,
                               input_data.employment_type_id) == 0
    assert range_type_score(score_card.scorecard_list[2].scores,
                            score_card.scorecard_list[2].missing,
                            input_data.years_employed_at_current_job) == 0
    assert range_type_score(score_card.scorecard_list[3].scores,
                            score_card.scorecard_list[3].missing,
                            input_data.gross_yearly_income) == 0
    assert score_sum(score_card.scorecard_list, score_card.intercept, input_data) == 203


def test_probability_of_default():
    k1 = 0.27882
    k2 = 0.014802
    assert probability_of_default(k1, k2, 1) == 1  # math.exp(0.27882 - 0.014802 * 1) = 1.3021516348193736 -> 1
    assert probability_of_default(k1, k2, 10) == 1  # math.exp(0.27882 - 0.014802 * 10) = 1.1397398105535637 -> 1
    assert probability_of_default(k1, k2, 100) == 0.3007788505650107
    assert probability_of_default(k1, k2, 150) == 0.1434914252389834


def test_calculate_scorecard():
    input_data = build_input_data(cc_00_application)
    score = score_sum(score_card.scorecard_list, score_card.intercept, input_data)

    assert score == 150
    assert probability_of_default(score_card.calibration_equation[0], score_card.calibration_equation[1], score) \
           == 0.1434914252389834
    assert calculate_scorecard(score_card, input_data) == Output(150, 0.1434914252389834, 'CC')

from src.application import build_input_data
from src.scorecard import *
from src.variables import Variable, VariableType
from tests.sample_data import get_sample_data

score_card = Scorecard(
    [
        ScorecardVariable(
            Variable('accomodation_type_id', VariableType.CATEGORY),
            [BandPoint([1.0], 54.0), 
             BandPoint([2.0, 3.0], -12.0), 
             BandPoint([4.0], 0.0)], 
            0.0
        ), 
        ScorecardVariable(
            Variable('employment_type_id', VariableType.CATEGORY), 
            [BandPoint([1.0], 42.0), 
             BandPoint([2.0], 0.0), 
             BandPoint([3.0], -4.0), 
             BandPoint([5.0], 20.0),
             BandPoint([4.0, 6.0, 7.0], 0.0)],
            0.0
        ),
        ScorecardVariable(
            Variable('unsecured_debt', VariableType.RANGE),
            [BandPoint([-math.inf, 0.0], 66.0),
             BandPoint([0.0, 6200.0], 47.0),
             BandPoint([6200.0, 45300.0], 33.0),
             BandPoint([45300.0, math.inf], 0.0)],
            0.0
        ),
        ScorecardVariable(
            Variable('gross_yearly_income', VariableType.RANGE),
            [BandPoint([-math.inf, 25200.0], -47.0),
                BandPoint([25200.0, 46800.0], 0.0),
                BandPoint([46800.0, math.inf], 0.0)],
            0.0
        )
    ],
    [0.296372, 0.010903],
    122.0,
    'UL'
)
ul_00_application = get_sample_data('UL_00.json')


def test_category_type_score():
    # Test category_type_score with bands:
    # [BandPoint([1.0], 54.0),
    #  BandPoint([2.0, 3.0], -12.0),
    #  BandPoint([4.0], 0.0)],
    category_scores = score_card.scorecard_list[0].scores
    assert category_type_score(category_scores, 0, 1) == 54
    assert category_type_score(category_scores, 0, 2) == -12
    assert category_type_score(category_scores, 0, 3) == -12
    assert category_type_score(category_scores, 0, 4) == 0
    assert category_type_score(category_scores, 0, None) == 0
    assert category_type_score(category_scores, 200, None) == 200


def test_range_type_score():
    # Test range_type_score with bands:
    # [BandPoint([-math.inf, 0.0], 66.0),
    #  BandPoint([0.0, 6200.0], 47.0),
    #  BandPoint([6200.0, 45300.0], 33.0),
    #  BandPoint([45300.0, math.inf], 0.0)],

    range_scores = score_card.scorecard_list[2].scores
    assert range_type_score(range_scores, 0, -1) == 66
    assert range_type_score(range_scores, 0, 0) == 66
    assert range_type_score(range_scores, 0, 5000) == 47
    assert range_type_score(range_scores, 0, 6200) == 47
    assert range_type_score(range_scores, 0, 40000) == 33
    assert range_type_score(range_scores, 0, 45300) == 33
    assert range_type_score(range_scores, 0, 46000) == 0
    assert range_type_score(range_scores, 0, None) == 0
    assert range_type_score(range_scores, 20, None) == 20


def test_score_sum():
    # Test score sum for application UL_00
    # "accomodation_type_id": 2,
    # "employment_type_id": 1,
    # "gross_yearly_income": 33000,
    # "unsecured_debt": 60000,
    # score_sum = 122 - 12 + 42 + 0 + 0 = 152
    input_data = build_input_data(ul_00_application)

    assert category_type_score(score_card.scorecard_list[0].scores,
                               score_card.scorecard_list[0].missing,
                               input_data.accomodation_type_id) == -12
    assert category_type_score(score_card.scorecard_list[1].scores,
                               score_card.scorecard_list[1].missing,
                               input_data.employment_type_id) == 42
    assert range_type_score(score_card.scorecard_list[2].scores,
                            score_card.scorecard_list[2].missing,
                            input_data.unsecured_debt) == 0
    assert range_type_score(score_card.scorecard_list[3].scores,
                            score_card.scorecard_list[3].missing,
                            input_data.gross_yearly_income) == 0
    assert score_sum(score_card.scorecard_list, score_card.intercept, input_data) == 152


def test_probability_of_default():
    k1 = 0.296372
    k2 = 0.010903
    assert probability_of_default(k1, k2, 1) == 1  # math.exp(0.27882 - 0.014802 * 1) = 1.3303858327834217 -> 1
    assert probability_of_default(k1, k2, 10) == 1  # math.exp(0.27882 - 0.014802 * 10) = 1.2060396800969453 -> 1
    assert probability_of_default(k1, k2, 100) == 0.4520655895741381
    assert probability_of_default(k1, k2, 152) == 0.2564339890817371


def test_calculate_scorecard():
    input_data = build_input_data(ul_00_application)
    score = score_sum(score_card.scorecard_list, score_card.intercept, input_data)

    assert score_sum(score_card.scorecard_list, score_card.intercept, input_data) == 152
    assert probability_of_default(score_card.calibration_equation[0], score_card.calibration_equation[1], score) \
           == 0.2564339890817371
    assert calculate_scorecard(score_card, input_data) == Output(152, 0.2564339890817371, 'UL')

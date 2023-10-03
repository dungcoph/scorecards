import math
from src.read_scorecards_from_excel import read_excel_to_df_map,\
    covert_excel_file_to_scorecards_map, get_scorecard_with_key


path = 'scorecards.xlsx'
scorecards_map = covert_excel_file_to_scorecards_map(path)


def test_read_excel_to_df_map():
    df_map = read_excel_to_df_map(path)
    first_value = next(iter(df_map.values()))
    assert first_value.iloc[0, 0] == 'Intercept'
    assert first_value.iloc[0, 3] == 203
    assert first_value.iloc[1, 0] == 'AccomodationTypeID'
    assert first_value.iloc[1, 1] == 1
    assert first_value.iloc[1, 3] == 33
    assert math.isnan(first_value.iloc[2, 0])
    assert first_value.iloc[2, 1] == '2|3'
    assert first_value.iloc[4, 1] == 'missing'
    assert first_value.iloc[11, 1] == '(-inf, 0]'
    assert first_value.iloc[17, 1] == '(35000, inf]'
    assert first_value.iloc[19, 0] == 'calibration_equation:'
    assert first_value.iloc[19, 1] == 'PD = exp(0.27882 - 0.014802 * score_sum)'


def test_covert_df_to_scorecards_map():
    cc_scorecard = scorecards_map['CC']
    first_key = next(iter(scorecards_map.keys()))
    cc_scorecard_list = cc_scorecard.scorecard_list
    accomodation_type_id_score = cc_scorecard_list[0].scores
    employment_type_id_score = cc_scorecard_list[1].scores
    years_employed_at_current_job = cc_scorecard_list[2].scores

    ul_scorecard = scorecards_map['UL']
    ul_scorecard_map = ul_scorecard.scorecard_list
    unsecured_debt_score = ul_scorecard_map[2].scores
    gross_yearly_income_score = ul_scorecard_map[3].scores

    assert first_key == 'CC'
    assert cc_scorecard.intercept == 203
    assert cc_scorecard.calibration_equation == [0.27882, 0.014802]
    assert cc_scorecard_list[0].missing == 0
    assert accomodation_type_id_score[0].band == [1]
    assert accomodation_type_id_score[0].point == 33
    assert accomodation_type_id_score[1].band == [2, 3]
    assert accomodation_type_id_score[1].point == -10
    assert accomodation_type_id_score[2].band == [4]
    assert accomodation_type_id_score[2].point == 0
    assert employment_type_id_score[0].band == [1]
    assert employment_type_id_score[0].point == 40
    assert employment_type_id_score[1].band == [2]
    assert employment_type_id_score[1].point == 0
    assert employment_type_id_score[4].band == [4, 6, 7]
    assert employment_type_id_score[4].point == 0
    assert years_employed_at_current_job[0].band == [-math.inf, 0]
    assert years_employed_at_current_job[1].band == [0, 2]
    assert years_employed_at_current_job[2].band == [2, math.inf]
    assert years_employed_at_current_job[0].point == -40
    assert years_employed_at_current_job[1].point == 0
    assert years_employed_at_current_job[2].point == 36

    assert ul_scorecard.intercept == 122
    assert unsecured_debt_score[0].band == [-math.inf, 0]
    assert unsecured_debt_score[1].band == [0, 6200]
    assert unsecured_debt_score[2].band == [6200, 45300]
    assert unsecured_debt_score[3].band == [45300, math.inf]
    assert unsecured_debt_score[0].point == 66
    assert unsecured_debt_score[1].point == 47
    assert unsecured_debt_score[2].point == 33
    assert unsecured_debt_score[3].point == 0
    assert ul_scorecard_map[2].missing == 0
    assert gross_yearly_income_score[0].band == [-math.inf, 25200]
    assert gross_yearly_income_score[1].band == [25200, 46800]
    assert gross_yearly_income_score[2].band == [46800, math.inf]
    assert gross_yearly_income_score[0].point == -47
    assert gross_yearly_income_score[1].point == 0
    assert gross_yearly_income_score[2].point == 0


def test_get_scorecard_with_key():
    scorecard = get_scorecard_with_key('CC', scorecards_map)
    assert scorecard.name == 'CC'
    assert scorecard.intercept == 203
    assert scorecard.calibration_equation == [0.27882, 0.014802]



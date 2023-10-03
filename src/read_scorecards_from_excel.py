"""
Create scorecards map from Excel file with an input is the path to the Excel file
Output of this is all scorecards that store in scorecards_map
"""

import pandas as pd
from src.utils import get_number_from_string, get_parent_dir
from src.variables import BandPoint, ScorecardVariable, VARIABLES_MAPPING, Scorecard


def read_excel_to_df_map(path: str) -> dict:
    # Read Excel file
    ex_file = pd.ExcelFile(get_parent_dir() + path)
    sheet_to_df_map = {}

    # Map each sheet to an element of sheet_to_df_map
    for sheet_name in ex_file.sheet_names:
        sheet_to_df_map[sheet_name] = ex_file.parse(sheet_name)

    return sheet_to_df_map


def covert_excel_file_to_scorecards_map(path: str) -> dict:
    # Read Excel file and convert it to a dict with all scorecards
    # Each scorecard will be one element:
    #   key is name of this scorecard
    #   value is class Scorecard

    # Read Excel file
    df_map = read_excel_to_df_map(path)

    # scorecards_map where store all scorecard
    # Each scorecard will be one element with key is name of this scorecard
    scorecards_map = {}

    # loop through all items of df_map
    # each item is a one type of scorecard
    for key, value in df_map.items():
        # Remove Scorecard in name of sheet
        scorecard_name = key.replace(' Scorecard', '')

        # scorecard is one that has type of Scorecard
        scorecard = Scorecard([], [], 0, scorecard_name)

        # scorecard_list is list of all scores for all variable in this scorecard
        scorecard_list = []

        # variable_score_list is a list of all score for one variable
        variable_score_list = []

        pre_variable = ''

        for i in range(len(value)):
            variable = value.iloc[i, 0]

            if variable == 'Intercept':
                # It is intercept row, get intercept point from column point
                scorecard.intercept = value.iloc[i, 3]
            elif variable == 'calibration_equation:':
                # It is calibration_equation row, get 2 number to calculate pd
                scorecard.calibration_equation = get_number_from_string(value.iloc[i, 1])
            else:
                if type(variable) is str:
                    # New variable
                    # Set new variable to be previous variable
                    pre_variable = variable
                else:
                    # If variable is not string, it is still same variable
                    # variable == nan now
                    # set pre_variable to variable
                    variable = pre_variable

                if value.iloc[i, 1] == 'missing':
                    scorecard_list.append(ScorecardVariable(VARIABLES_MAPPING[variable],
                                                            variable_score_list,
                                                            value.iloc[i, 3]))
                    # Reset variable_score_list to store for new variable
                    variable_score_list = []
                else:
                    # append variable_score_list with bands in column bands and point in column point
                    variable_score_list.append(BandPoint(get_number_from_string(str(value.iloc[i, 1])),
                                                         value.iloc[i, 3]))

        # Finish loop for all rows in one sheet
        # Set scorecard_list in scorecard
        scorecard.scorecard_list = scorecard_list

        # Set scorecard with key is sheet_name to scorecard_map
        scorecards_map[scorecard_name] = scorecard

    return scorecards_map


def get_scorecard_with_key(key: str, scorecards_map: dict) -> Scorecard:
    return scorecards_map.get(key)

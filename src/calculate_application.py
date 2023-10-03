from src.application import Application, build_input_data
from src.read_scorecards_from_excel import covert_excel_file_to_scorecards_map, get_scorecard_with_key
from src.scorecard import calculate_scorecard


def calculate_output(application: Application) -> Application:
    print(application)
    # Get scorecards_map of all type scorecard from Excel file
    path_to_excel_scorecard = 'scorecards.xlsx'
    scorecards_map = covert_excel_file_to_scorecards_map(path_to_excel_scorecard)

    # Prepare input data to calculate
    input_data = build_input_data(application)

    # Get correct scorecard type depend on application
    scorecard = get_scorecard_with_key(input_data.product_type, scorecards_map)

    # Calculate score and pd for this application
    output = calculate_scorecard(scorecard, input_data)

    # set result to application to return
    application.output = output

    return application

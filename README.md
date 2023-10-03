# Bank Norwegian Interview Task - 2023


## How to test
1. Go to the application folder.
2. Open cmd on this folder
3. Python version is 3.10.11
4. Create a virtual environment for the app:
	- python3 -m venv .venv
	- .venv\scripts\activate
5. Install the dependencies:
	- pip install -r requirements.txt
6. Run the app:
	- flask run
7. Testing using Postman app:
    - Import collection postman/BN.postman_collection.json to Postman
    - There are 3 request: 
      - 2 request for single customer
      - 1 request for multiple customers as same time

## App logic

### Prepare scorecards.xlsx(interview_task_sample_scorecards.xlsx) file
- Rename the Excel file to scorecards.xlsx and put it in the folder of application.
- Remove the row between table of scorecard and calibration_equation so there is no empty row between these

### read_scorecards_from_excel.py
- Read data from scorecards.xlsx(interview_task_sample_scorecards.xlsx) and convert it to a dictionary with:
  - key: name of scorecard. it will be 'CC' or 'UL'
  - value: whole scorecard with all variables name, bands, point and constants for calibration_equation
- This implementation have advantage:
  - Prevent implementation bugs while going from these excel specifications to code because we don't need to put in manually.
  - Can handle a lot more scorecards without to change in the code. Just need to add more sheets in these Excel file.
- The result of this can be saved to database so the app don't need to compute scorecard model everytime

### VARIABLES_MAPPING constant
- Mapping between name of variables in Excel file and in input with extra information about which type of variable.
- For this one, there are 2 types of variable:
  - Category for variable accomodation_type_id and employment_type_id
  - Range for years_employed_at_current_job, gross_yearly_income and unsecured_debt
- Combine with scorecards map from read_scorecards_from_excel, the app can combine correct variable with scorecard.
- So if there are more variables, we just need update this mapping to make sure the app look up correct input with scorecard.
- This will help to increase the amount of input with very limited change in code
- This mapping can also be saved in database

### Calculate for customer
- When the app gets a request, it can get the correct scorecard by key with input.product_type. 
- The key is set to same with input.product_type so scorecard type can get automatic with input.product_type
  - get_scorecard_with_key(input_data.product_type, scorecards_map)
- Calculate score_sum(scorecard.py):
  - score_sum is calculate with the chose scorecard and input
  - Score is calculate is with 2 different types variable and all input data retrieve from input with help of variable name and variable type in mapping
  - These file is general enough that it can be used for all scorecards. Just need put in scorecard model that we have from read_scorecards_from_excel.py

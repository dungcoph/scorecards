import math
import pathlib
import re
from datetime import datetime
from typing import Union
from dateutil.relativedelta import relativedelta


def convert_date_to_years(date_since: Union[str, None]) -> Union[int, None]:
    if date_since is None:
        return None
    else:
        date_format = '%Y-%m-%dT%H:%M:%S'
        start_date = datetime.strptime(date_since, date_format)
        today = datetime.today()
        return relativedelta(today, start_date).years


def get_number_from_string(str_input: str) -> list[float]:
    pattern = r'[\d]*[.][\d]+|[\d]+|[\-]*inf'
    str_array = re.findall(pattern, str_input)
    result = []

    for numeric_string in str_array:
        if numeric_string == '-inf':
            result.append(-math.inf)
        elif numeric_string == 'inf':
            result.append(math.inf)
        else:
            result.append(float(numeric_string))

    return result


def get_parent_dir() -> str:
    current_dir = pathlib.Path(__file__).parent
    return str(pathlib.Path(current_dir).parent) + '/'

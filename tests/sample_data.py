import json
from munch import DefaultMunch
from src.application import Application
from src.utils import get_parent_dir


def get_sample_data(file_name: str) -> Application:
    with open(get_parent_dir() + 'sample_inputs/' + file_name, 'r') as sample_input:
        sample_input_data = json.load(sample_input)
        return DefaultMunch.fromDict(sample_input_data)

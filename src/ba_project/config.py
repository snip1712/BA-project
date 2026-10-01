import logging
import pathlib

logging.basicConfig(level=logging.INFO)

## Configuration file for the BA project.
''' 
this file contains configuration settings for the BA project, including paths to data files and output files.
it also includes functions to retrieve these paths, which can be used throughout the project to ensure consistency and avoid hardcoding file paths.
args:
    None
returns:
    pathlib.Path: The path to the data file or output file, depending on the function called.
use examples:
from ba_project.config import get_data_file_path, get_output_file_path
data_file_path = get_data_file_path()
output_file_path = get_output_file_path()

'''
def get_data_file_path() -> pathlib.Path:
    """
    Get the path to the data file.

    Returns:
        pathlib.Path: The path to the data file.
    """
    logging.info("Getting data file path")
    return pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "data.ods"

def get_output_file_path() -> pathlib.Path:
    """
    Get the path to the output file.

    Returns:
        pathlib.Path: The path to the output file.
    """
    logging.info("Getting output file path")
    return pathlib.Path(__file__).resolve().parent.parent.parent /"output"


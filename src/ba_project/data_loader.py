import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

## Function to load data from a spreadsheet file into a pandas DataFrame

def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load data from a spreadsheet file into a pandas DataFrame.

    Args:
        file_path (Path): The path to the spreadsheet file."""
    
    logging.info(f"Loading data from {file_path}")
   
    return pd.read_excel(file_path)
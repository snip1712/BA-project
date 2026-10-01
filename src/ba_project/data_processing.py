
import pandas as pd
import logging
from ba_project.config import get_data_file_path
from ba_project.data_loader import load_data
from ba_project.visualization import create_visualizations 


logging.basicConfig(level=logging.INFO)

logging.info("Loading data from the data file")
df = load_data(get_data_file_path())
logging.info(f"Data loaded successfully. DataFrame shape: {df.shape}")


# the final deliverable code starts here -----------------------------------------------------------------------------------------------------------------------------
logging.info("Calculating tier eligible passenger ratios and creating visualizations")
# step 1: calculate the ratio of tier eligible passengers to total passengers for each flight
Passengers_sum = df["FIRST_CLASS_SEATS"] + df['BUSINESS_CLASS_SEATS'] + df['ECONOMY_SEATS']
df["t1_ratio"] = (df["TIER1_ELIGIBLE_PAX"] / Passengers_sum)*100
df["t2_ratio"] = (df["TIER2_ELIGIBLE_PAX"] / Passengers_sum)*100
df["t3_ratio"] = (df["TIER3_ELIGIBLE_PAX"] / Passengers_sum)*100

# step 2: group the data by ARRIVAL_REGION, HAUL, and TIME_OF_DAY and calculate the mean of the ratios
grouped = df.groupby(['ARRIVAL_REGION', 'HAUL', 'TIME_OF_DAY'])[['t1_ratio', 't2_ratio', 't3_ratio']]

# step 3: create visualizations using the grouped data and the raw data
create_visualizations(raw = df, df = grouped.agg(
    t1_mean=("t1_ratio", "mean"),
    t2_mean=("t2_ratio", "mean"),
    t3_mean=("t3_ratio", "mean"),
    count=("t1_ratio", "size")).reset_index()
)

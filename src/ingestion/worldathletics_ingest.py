# %%
from data_lake_utils import upload_file_to_data_lake

# static dataset (web scraped, used parse.py script to extract values from html file)
file_path = "./worldathletics/mens_100m_race_results_2022_30_34.csv"
upload_file_to_data_lake(file_path)
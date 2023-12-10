# %%
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
import pandas as pd
import os
import zipfile

from data_lake_utils import upload_file_to_data_lake

api = KaggleApi()
api.authenticate()

def rename_and_upload_file(original_path, new_file_name):
    new_file = original_path.parent / new_file_name
    original_path.rename(new_file)
    upload_file_to_data_lake(new_file)

def add_year_column(csv_file, year):
    df = pd.read_csv(csv_file)
    df['csvfilename_year'] = year
    return df

def process_single_file_dataset(dataset, file_name, new_file_name):
    out_path = Path.cwd() / 'kaggle/api/datasets'
    os.makedirs(out_path, exist_ok=True)

    api.dataset_download_files(dataset, path=out_path, unzip=True)

    original_file = out_path / file_name
    if original_file.exists():
        rename_and_upload_file(original_file, new_file_name)
    else:
        print(f"File not found: {original_file}")

def process_multi_file_dataset(dataset, new_file_name):
    out_path = Path.cwd() / 'kaggle/api/datasets/multi'
    os.makedirs(out_path, exist_ok=True)

    api.dataset_download_files(dataset, path=out_path, unzip=True)

    dataframes = []

    for csv_file in out_path.glob('*.csv'):
        # extract the year from a file name in the format "yyyy_combine.csv"
        year = csv_file.stem.split('_')[0]  # Extracts the year from the file name
        df_with_year = add_year_column(csv_file, year)
        dataframes.append(df_with_year)

    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_csv_path = Path.cwd() / f'kaggle/api/datasets/{new_file_name}'
    combined_df.to_csv(combined_csv_path, index=False)
    
    rename_and_upload_file(combined_csv_path, new_file_name)

# For the Crossfit single CSV file dataset
process_single_file_dataset('ulrikthygepedersen/crossfit-athletes', 'athletes.csv', 'CrossfitAthletes.csv')

# For the NFL combine multi CSV files dataset
process_multi_file_dataset('mitchellweg1/nfl-combine-results-dataset-2000-2022', 'NFLCombineResults.csv')
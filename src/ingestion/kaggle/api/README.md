# Kaggle API Tips & Pointers
Datasets are prepped and ready to go. Use the kaggle API and CLI for quick search of availble datasets

Example command:
kaggle datasets list -s athletes

Found two interesting datasets of compiled athlete performance measurements
- ulrikthygepedersen/crossfit-athletes
- mitchellweg1/nfl-combine-results-dataset-2000-2022

## Single file vs. Multi-file datasets
Some datasets on Kaggle are provided as one csv file. Others might contain multi-file datasets. For example, the Crossfit data was provided as a single file (athletes.csv.zip) and the NFL Combine results were provided as multiple csv files (2022_combine.csv, 2021_combine.csv, etc.)
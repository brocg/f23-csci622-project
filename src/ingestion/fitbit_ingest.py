import os
import requests
import pandas as pd

from data_lake_utils import upload_file_to_data_lake

fitbit_host = "https://api.fitbit.com"
fitbit_access_token = os.getenv('FITBIT_ACCESS_TOKEN')

if not fitbit_host or not fitbit_access_token:
    raise ValueError("Required environment variables not set.")

headers = {
    'Authorization': f'Bearer {fitbit_access_token}'
}

profile_endpoint = "/1.2/user/-/sleep/date/2023-11-04.json" # sleep log for specific date

response = requests.get(f"{fitbit_host}{profile_endpoint}", headers=headers)

if response.status_code == 200:
    profile_data = response.json()

    if 'user' in profile_data:
        user_df = pd.DataFrame([profile_data['user']])
        user_df.to_csv("fitbit/api/datasets/FitbitUserProfile.csv", index=False)
   
    elif 'sleep' in profile_data:
        user_df = pd.DataFrame([profile_data['sleep']])
        user_df.to_json("fitbit/api/datasets/FitbitSleepLog.json", orient='records', lines=True)

    elif 'summary' in profile_data:
        user_df = pd.DataFrame([profile_data['summary']])
        user_df.to_csv("fitbit/api/datasets/FitbitDailyActivity.csv", index=False)

    else:
        print("key for [profile_data['xxx'] not found, check response")
else:
    print(f"Failed to fetch user data: {response.status_code}")
    print(response.text)

file_path = "fitbit/api/datasets/FitbitSleepLog.json"
upload_file_to_data_lake(file_path)
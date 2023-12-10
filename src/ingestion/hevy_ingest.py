import os
import requests
import pandas as pd

from data_lake_utils import upload_file_to_data_lake

hevy_host = "https://api.hevyapp.com"
hevy_auth_token = os.getenv('HEVY_AUTH_TOKEN')
hevy_api_key = os.getenv('HEVY_API_KEY')

if not hevy_host or not hevy_auth_token or not hevy_api_key:
    raise ValueError("Required environment variables not set.")

headers = {
    'x-api-key': hevy_api_key,
    'auth-token': hevy_auth_token,
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'okhttp/4.9.3',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

profile_endpoint = "/workouts_batch/0"

response = requests.get(f"{hevy_host}{profile_endpoint}", headers=headers)

if response.status_code == 200:

    profile_data = response.json()
    user_df = pd.DataFrame(profile_data)
    user_df.to_csv("hevy/api/datasets/HevyWorkouts.csv", index=False)

else:
    print(f"Failed to fetch user data: {response.status_code}")
    print(response.text)

file_path = "hevy/api/datasets/HevyWorkouts.csv"
upload_file_to_data_lake(file_path)
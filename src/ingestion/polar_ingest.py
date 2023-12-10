import os
import requests
import pandas as pd

from data_lake_utils import upload_file_to_data_lake

polar_host = "https://www.polaraccesslink.com"
polar_access_token = os.getenv('POLAR_ACCESS_TOKEN')
polar_api_key = os.getenv('POLAR_API_KEY')
polar_user_id = os.getenv('POLAR_USER_ID')

if not polar_host or not polar_access_token:
    raise ValueError("Required environment variables not set.")

headers = {
    'Authorization': f'Bearer {polar_access_token}'
}

profile_endpoint = "/v3/exercises"

response = requests.get(f"{polar_host}{profile_endpoint}", headers=headers)

if response.status_code == 200:

    profile_data = response.json()
    user_df = pd.DataFrame(profile_data)
    user_df.to_csv("polar/api/datasets/PolarExercises.csv", index=False)

else:
    print(f"Failed to fetch user data: {response.status_code}")
    print(response.text)

file_path = "polar/api/datasets/PolarExercises.csv"
upload_file_to_data_lake(file_path)
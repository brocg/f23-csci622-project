# %%
from bs4 import BeautifulSoup
import pandas as pd
import re

# ChatGPTv4 (Nov '23) assisted code to parse the HTML table using Beautiful Soup

# Define a function to clean the text, remove newlines, and extra spaces
def clean_text(text):
    return re.sub(r'\s+', ' ', text.replace('\n', ' ').strip())

# Define a function to extract the athlete's name and age
def extract_athlete_name_and_age(athlete_info):
    athlete_info = clean_text(athlete_info)
    parts = athlete_info.split('(')
    if len(parts) == 2:
        name = parts[0].strip()
        age = parts[1].replace(')', '').strip()
    else:
        name = athlete_info.strip()
        age = ''
    return name, age

# Define a function to extract data from a row
def extract_data_from_row(row):
    tds = row.find_all('td')
    if len(tds) != 6:
        return None  # Skip rows that do not have 6 data cells
    athlete_info = clean_text(tds[3].a.input['value'])
    name, age = extract_athlete_name_and_age(athlete_info)
    row_data = {
        'Rank': clean_text(tds[0].get_text()),
        'Performance': clean_text(tds[1].input['value']),
        'Wind': clean_text(tds[2].input['value']),
        'Athlete': name,
        'Age': age,
        'Country': clean_text(tds[4].input['value']),
        'Location': clean_text(tds[5].input['value']).rsplit(' on ', 1)[0],
        'Date': clean_text(tds[5].input['value']).rsplit(' on ', 1)[1]
    }
    return row_data

# Initialize a list to hold the extracted data for each row
data_list = []

# Define the path to your HTML file
html_file_path = 'tableathletics.html'

# Open the HTML file and parse it with BeautifulSoup
with open(html_file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Extracting the data for each row
for row in soup.find_all('tr', class_="ranktablerow"):
    data = extract_data_from_row(row)
    if data:
        data_list.append(data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
csv_file_path = 'mens_100m_race_results_2022_30_34.csv'
df.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")

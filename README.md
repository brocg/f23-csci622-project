# CSCI 622 Project - Brock
# Athlete Performance Dashboard

- The Athlete Performance Dashboard aims to help individuals improve their athletic performance by making data-driven decisions, staying motivated, and maintaining a holistic approach to training and well-being.

## How to Interact With the Dashboard
- Open the dashboard here: https://brocg.github.io/athlete-performance-dashboard (login with @ndus.edu creds)

- **Click on a day on the calendar**. It will highlight the selected day, and display the corresponding metrics for heart rate training zone and sleep. The tooltip on the day shows workout notes.

> ![Dashboard Demo Day Selection](/SupplementaryInfo/screenshots/dashboard-demo-day-selection.gif)

# Getting Started
This repo contains all files used to create the dashboard. See SupplementaryInfo directory for the PowerBI file and 3 datasets (HevyWorkouts, FitbitSleepLog, PolarExercises). See the "CSCI 622 - Project Recap Brock.pdf" for a good overview of what steps were involved in designing this dashboard.

## View Dashboard Online
1. Visit https://brocg.github.io/athlete-performance-dashboard (works best in Chrome/Edge)
2. If prompted for login, use @ndus.edu credentials (might require agreeing to a prompt for free trial)

## View Dashboard Locally (using PowerBI)
If you're interested an offline local setup in PowerBI, follow these steps.

I'm currently hosting the data on Azure container as publically accessible so you shouldn't need any access token for this to work. 

1. Download [PowerBI Desktop](https://powerbi.microsoft.com/en-us/desktop/)
2. Open "HevyWorkoutsBI.pbix" file ([download here](https://drive.google.com/file/d/1MkpzdAuhd_52cgjENi1LC1JIHep5rx-5/view?usp=sharing), also in this repo)
3. Ensure the 3 datasource files are pulling from this Azure Blob Service (https://samplestorepowerbi.blob.core.windows.net/f23-proj/). You can verify the container address by going to File > Options and Settings > Data Source Settings
4. Click "Refresh" on Ribbon, all data should load in : )

For further customization, I recommend using the 3 files in "SupplementaryInfo/PowerBI/raw-datafiles" as your data sources (so it doesn't rely on the Azure Blob container). Then you have complete control to edit things as you see fit. It'll require rejoining the three tables, and a few other tweaks, but should be doable.


# Project Overview / Motivation for Developing

## 2 Primary Athletic Goals
![Run Faster Jump Higher](/SupplementaryInfo/screenshots/run-faster-jump-higher.png)

1. **Jump Higher**, measuring standing vertical leap (using a [vertec](https://www.power-systems.com/shop/product/vertec#lg=1&slide=2))
    - Target: 33"
    - Current: 27.5"
2. **Run Faster**, measuring sprint speed in 100M dash (using [handheld stopwatch](https://www.walmart.com/ip/Athletic-Works-Digital-Stopwatch-Black/984512262?athbdg=L1600) + [SprintTimer App](https://apps.apple.com/us/app/sprinttimer-photo-finish/id430807521))
    - Target: 11.80 seconds
    - Current: 12.35 seconds (as of August 2023)

These 2 performance metrics will be measured once a month and manually logged.


### How to measure improvements with data?
Improving vertical jump height requires a combination of strength training, plyometric exercises, technique refinement, and consistent monitoring. Here's a list of possible types of data to collect:

1. Strength Training
2. Plyometric Training
3. Jumping/Sprinting Technique
4. Recovery
5. Nutrition

## Problem Statement
- Athletes and fitness enthusiasts often struggle to optimize their training regimens due to the fragmented nature of health and performance data. 
- They spend valuable time collecting data from various sources like fitness trackers and apps (e.g., Fitbit, Apple Watch, MyFitnessPal, etc.), but this process often results in scattered data across different systems. 

  - Common Pain Points
    - **Manual data entry is time-consuming**
      - Collecting and managing data from multiple sources is a time-consuming task that takes athletes away from their primary focus: training.
      - Spreadsheets are often used to track metrics, but can often become outdated, overly complex, and not easy to update while training in the gym, competing in the field, etc.
    - **Using multiple hardware devices/subscriptions becomes expensive**
      - Owning and maintaining various hardware devices and subscribing to multiple fitness apps can be costly. In general, the goal is to get the most value out of the hardware devices and spend the least amount of money as possible. 
    - **Limited access to historical data**
      - As an athlete it's valuable to see trends over days, weeks, months, and even years. However, over the years the hardware devices and subscriptions change, resulting in data that's lost or unrecoverable. 
  
- Ideally a solution should be provided to see ALL your previous data, regardless of the data source. 
    
## Core Feature to Develop: One Dashboard View
- Integrate *all* health input data from various sources and provide in a single view on a web page
  - Ex: [https://brocg.github.io/athlete-performance-dashboard](https://brocg.github.io/athlete-performance-dashboard)
- Provide data analytics insights
  - Better understand how nutrition, sleep, and workouts are impacting performance. Answer questions such as:
      - How's my sleep been over the last 2 weeks?
      - How am I recoverying from my workouts?
      - What's my current bodyweight?
      - Am I gaining lean muscle?
      - How are my squat/deadlift progressions looking? Do I need to adjust weights?
      - Is my heart rate healthy?
      - Am I eating enough? What's my caloric intake? Am I getting enough protein? 
      - What's my completed workout history for the month?
      - etc.

## Ingestion
Each ingestion file pulls from it's respective API, saves the response, then uploads to ADLS. 

Files used for ingestion:
- ingest_fitbit.py
- ingest_hevy.py
- ingest_polar.py
- kaggle_ingest.py
- worldathletics_ingest.py

## Transformation

After data is ingested, it's verified using Azure Data Bricks (ADB). This requires spinning up a cluster (~5 minute process). ADB is used to useful to see shape/structure using Pyspark. 

![Verifying structure of data with ADB](/SupplementaryInfo/screenshots/azure-data-bricks-verifying-data.png)

This is a manual process, but good for making sure as data changes (i.e. REST APIs of Fitbit, Hevy, and Polar evolve) it will show what's going on.

Then the majority of data transformations take place within PowerBI. There are 3 files pulled into PowerBI through connecting to the Azure Blob storage account.
1. PolarHR
2. HevyWorkouts
3. FitbitSleepLog

The data model in PowerBI is simple. One table for each file.
![Data Model Power BI](/SupplementaryInfo/screenshots/data-model-powerBI.png)


Each file goes through a series of data transformations, but all original data is kept intact. For example, FitbitSleep log is provided as JSON file, and using PowerBI transform into a .csv file, and then add an additional column named "total_hours_sleep" to get hours slept each night in hours (e.g. 8.3).

![Data Model Power BI](/SupplementaryInfo/screenshots/example-data-transformation-total-hours-sleep.png)

## Serving

All visuals served through PowerBI. Dashboard is made of 6 key components:

| # | Name                         | PowerBI Visual Type                                          |
|--------|------------------------------|-------------------------------------------------------------|
| 1      | Training Session Date        | Slicer                                                       |
| 2      | Training Session Calendar    | [Calendar Visual by MAQ Software](https://maqsoftware.com/resources/Power-BI-custom-visuals/Calendar) - PowerBI Certified |
| 3      | Polar H10 Heart Rate Data    | Matrix                                                       |
| 4      | Heart Rate Training Zones 1-5| *Python visual                                                |
| 5      | Fitbit Sleep Log Data        | Card                                                         |
| 6      | Sleep Efficiency             | *Python Visual                                                |


![Components of BI Dashboard](/SupplementaryInfo/screenshots/components-of-dashboard-powerbi.png)

*The 2 Python visuals both rely on custom code for generating the graphs. In the online view, this takes a few seconds to load in. This could be optimized, but does a nice job showing the gist of what the visuals are after. Python was used in these visuals to have control and complete customization of the labels (labels show specifi bpm and total hours of sleep rounded to nearest tenth).

## Key takeaways from visuals
### Heart Rate Training Zones
> ![Heart Rate Training Zones](/SupplementaryInfo/screenshots/example-heart-rate-training-zones-explained.png)
- **More green dots in Zones 2 & 3 = better for higher intensity training.**
At a glance I can see what the overall training intensity of a workout is. For example, if bmp is averaging below 114bpm (upperbound of Zone1), then I know it's relatively light intensity. Not bad per say, but it's important when viewing the aggregated view of workouts, there are training sessions landing in Zones 2 and 3.

### Sleep Efficiency Visual
> ![Sleep Efficiency](/SupplementaryInfo/screenshots/example-explaining-sleep-visual.png)
- **More blue filling up the bar = higher sleep efficiency. Target > 8 hours total sleep.**
At a glance I can see how I slept the previous night on the day of that particular training session. 

- **While Fitbit provides it's own "sleep score", I prefer my own metric on the label of the blue bar chart**. Looking at when I slept 9.4 hours, with .9 hrs awake (9%), and 8.5 hours asleep (91%)...I'd simply call that 91% sleep efficiency. Fitbit takes more factors into account, although I'm not sure what. I display Fitbit's sleep effiency score above the bar chart.

- **Why does this matter?** Knowing how well I slept gives me a good guage for intensity going into training sessions. I would avoid doing a taxing workout (i.e. Zone 4) if I knew I was running on 4 hours of sleep. I'd like to improve this metric by seeing longer stretches of sleep. For example, seeing a 14 day rolling average and calculating my sleep debt would be cool (similar to https://www.risescience.com/).

## Data Sources

### Dynamic
- New data provided anytime devices are synced and workouts are completed

| Data Source | Data Source | Key Data | Additional Data | Access Method | Rank |
|-------------|------------------|----------|-----------------|---------------|----------|
| Fitbit | Wearable | Sleep log | Daily Activity Summaries | API | Primary |
| Hevy | Fitness App | Total Volume Lifted | Workout count, training session notes | API | Secondary |
| Polar | Wearable | Average Heart Rate | Cardio load, measuring time in HRMAX zones 1-5 | API | Secondary |

### Static
- Data is historical, remains the same. Plan to use for age-adjusted performance benchmarks, specifically 100M dash and vertical leap

| Data Source | Data Source | Key Data | Additional Data | Access Method | Rank |
|-------------|------------------|----------|-----------------|---------------|----------|
| Crossfit           | Kaggle          | Deadlift         | Backsquat, 400M, training background   | API            | Secondary   |
| NFL Combine        | Kaggle         | Vertical Leap | Historical Combine Data, Player Measurements  | API            | Secondary |
| World Athletics | Website          | 100M Race Results | Country, Location            | Web Scraping   | Secondary  |


### Primary Datasource: [Fitbit Web API](https://dev.fitbit.com/build/reference/web-api/) 
  - Fitbit device being used: [Fitbit Inspire 2](https://www.fitbit.com/global/fi/products/trackers/inspire2)
  - Type of datasource: Dynamic, data is synced daily (intraday polling available for personal-use)

- The Fitbit Web API is free and works with any fitbit wearable. As of 2023, there's 25+ fitbit trackers supported by Google.

![Fitbit devices](/SupplementaryInfo/screenshots/fitbit-trackers-inspire2.png)

### Fitbit Web API Explorer
- The [Fitbit Web API Explorer](https://dev.fitbit.com/build/reference/web-api/explore/), built using Swagger UI, is used for testing the Web API endpoints against a Fitbit user's personal data.

  - https://dev.fitbit.com/build/reference/web-api/explore/

  - Documentation: [Web API Reference](https://dev.fitbit.com/build/reference/web-api/)

    - Provides near real-time data (last 15min,30min,1hr) on metrics like heart rate, speed, distance, and more

    - Examples of API endpoints (18+ scope categories in total)
        - activity
        - location
        - respiratory_rate
        - temperature
        - cardio_fitness
        - nutrition
        - settings
        - weight
        - electrocardiogram
        - oxygen_saturation
        - sleep
        - heartrate
        - profile
        - social


### Secondary Datasources:
  - [Hevy](https://hevy.com/) - iOS/Android app, Workout Tracker & Planner Gym Weight Lifting
    - Data can be exported as .csv file via the app or website
    - Testing with experimental API access (https://api.hevyapp.com/)

  - [Polar H10](https://www.polar.com/us-en/sensors/h10-heart-rate-sensor/) - heart rate sensor, well known for its accuracy.
    - [Polar Accesslink API v3](https://www.polar.com/accesslink-api/#polar-accesslink-api)
      - Antropometrics
      - Energy expenditure
      - Heart rate analytics
      - Physical activity
      - Physical performance
      - Physiological load
      - Sleep analytics

### Other Possible Datasources:

- On-device APIs
  - Apple Watch Series 5
    - Healthkit
    - Workouts
    - Journal

- Web APIs
  - Strava
  - Tummee
  - MyFitness Pal

- Other Possible Manual Data Integrations (via data export)
  - Cronometer - Food
  - Levels - CGM (Freestyle Libre)
  - SprintTimer - Sprint Interval Splits
  - RISE/Sleepio - apps for sleep tracking
  - Nike Run Club - running
  - Workoutdoors - outdoor workouts
  - Downdog - yoga
  - Gaia GPS - hiking
  - Alltrails - hiking
  - Headspace - Meditation
  - MyRadar - hyperlocal weather
  - Trainerize - training log (70 previous workouts stored)
  - TrueCoach - training log (30 previous workouts stored)

- Other Custom APIs
  - Notion
  - Google Sheets
  - TestFlight iOS
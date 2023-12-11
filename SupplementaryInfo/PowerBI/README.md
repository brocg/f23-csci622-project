[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12440975&assignment_repo_type=AssignmentRepo)
# CSCI 622 Project - Brock
# Athlete Performance Dashboard

- The Athlete Performance Dashboard aims to help individuals improve their athletic performance by making data-driven decisions, staying motivated, and maintaining a holistic approach to training and well-being.

# Getting Started
This repo contains all files used to create the dashboard. See SupplementaryInfo directory for the PowerBI file. See the "CSCI 622 - Project Recap Brock.pdf" for a good overview of steps involved to create this.

Datsource files are stored in Azure Blob service. Some data is semi-sensitive, so need to scrub before providing public access. You can view the dashboard online, though.

## View Dashboard Online
1. Visit https://brocg.github.io/athlete-performance-dashboard
2. If prompted for login, use @ndus.edu credentials (might require agreeing to prompt for free trial)

## View Dashboard Locally (using PowerBI)
1. Download [PowerBI Desktop](https://powerbi.microsoft.com/en-us/desktop/)
2. Open "HevyWorkoutsBI.pbix" file ([download here](https://drive.google.com/file/d/1MkpzdAuhd_52cgjENi1LC1JIHep5rx-5/view?usp=sharing), also in this repo)

# Project Overview / Motivation for Developing

## 2 Primary Athletic Goals
![Run Faster Jump Higher](/SupplementaryInfo/screenshots/run-faster-jump-higher.png)

1. Jump Higher, measuring standing vertical leap (using a [vertec](https://www.power-systems.com/shop/product/vertec#lg=1&slide=2))
    - Target: 33"
    - Current: 27.5"
2. Run Faster, measuring sprint speed in 100M dash (using [handheld stopwatch](https://www.walmart.com/ip/Athletic-Works-Digital-Stopwatch-Black/984512262?athbdg=L1600) + [SprintTimer App](https://apps.apple.com/us/app/sprinttimer-photo-finish/id430807521))
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
      - As an athlete it's valuable to see trends over days, weeks, months, and even years. Howevever, over the years the hardware devices and subscriptions change, resulting in data that's lost or unrecoverable. 
  
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
Each inegstion file pulls from it's respective API, saves the response, then uploads to ADLS. 

Files used for ingestion:
- ingest_fitbit.py
- ingest_hevy.py
- ingest_polar.py
- kaggle_ingest.py
- worldathletics_ingest.py

## Transformation

After data is ingested, it's verified using Azure Data Bricks (ADB). This requires spinning up a cluster (~5 minute process). ADB is used to useful to see shape/structure using Pyspark. This is a manual process, but good for making sure as data changes (i.e. REST APIs of Fitbit, Hevy, and Polar evolve) it will show what's going on.

Then the majority of data transformations take place within PowerBI. There are 3 files pulled into PowerBI through connecting to the Azure Blob storage account.
1. PolarHR
2. HevyWorkouts
3. FitBitSleepLog

The data model in PowerBI is simple. One table for each file.
![Data Model Power BI](/SupplementaryInfo/screenshots/data-model-powerBI.png)


Each file goes through a series of data transformations, but all original data is kept intact. For example, FitbitSleep log is provided as JSON file, and using PowerBI transform into a .csv file, and then add an additional column named "total_hours_sleep" to get hours slept each night in hours (e.g. 8.2).

## Serving

All visuals served through PowerBI. Dashboard is made of 6 key components

![Components of BI Dashboard](/SupplementaryInfo/screenshots/components-of-powerbi-dashboard.png)

1. Trainining Session Date (Slicer)
2. Training Session Calendar ([Calendar Visual by MAQ Software](https://maqsoftware.com/resources/Power-BI-custom-visuals/Calendar) - PowerBI Certified)
3. Polar H10 Heart Rate Data (Matrix)
4. Heart Rate Training Zones 1-5 (Python visual)
5. Fitbit Sleep Log Data (Card)
6. Sleep Efficiency (Python Visual)

The 2 Python visuals both rely on custom code for generating the graphs. In the online view, this takes a few seconds to load in. This could be optimized, but does a nice job showing the gist of what the visuals are after. More green dots in Zone 3 = better for higher intensity training. And more blue for sleep = higher sleep effiency. Python was used for complete customization of the labels (to see specifically hours of sleep and bpm).


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

![Fitbit devices](/SupplementaryInfo/screenshots/fitbit-trackers.png)

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
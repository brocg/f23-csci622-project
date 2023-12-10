# Databricks notebook source
# Add imports, read in data to analyze
import json
import matplotlib.pyplot as plt
from pyspark.sql.functions import sum, desc, isnull, col, avg, count, when, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark.conf.set(
    "fs.azure.account.key.assignment1store.dfs.core.windows.net",
    dbutils.secrets.get(scope="DatabricksSetupScope", key="MySecret"))

uri = "abfss://assignment1@assignment1store.dfs.core.windows.net/"

# Fitbit
fitbit_daily_activity_df = spark.read.csv(uri + 'data/f23-proj/FitbitDailyActivity.csv', header=True)
fitbit_sleep_log_df = spark.read.json(uri + 'data/f23-proj/FitbitSleepLog.json')
fitbit_user_profile_df = spark.read.csv(uri + 'data/f23-proj/FitbitUserProfile.csv', header=True)

# Hevy
hevy_workouts_df = spark.read.csv(uri + 'data/f23-proj/HevyWorkouts.csv', header=True)

# Polar
polar_exercises_df = spark.read.csv(uri + 'data/f23-proj/PolarExercises.csv', header=True)

# Kaggle datasets (static)
crossfit_athletes_df = spark.read.csv(uri + 'data/f23-proj/CrossfitAthletes.csv', header=True)
nfl_combine_results_df = spark.read.csv(uri + 'data/f23-proj/NFLCombineResults.csv', header=True)

# World Masters Athletics (static)
world_athletics_df = spark.read.csv(uri + 'data/f23-proj/mens_100m_race_results_2022_30_34.csv', header=True)

# COMMAND ----------

# MAGIC %md
# MAGIC # Display Fitbit Data
# MAGIC Sleep log is most important file. This is the most valuable data (at the end of the JSON file response). 
# MAGIC
# MAGIC ```
# MAGIC logId": 43358421833,
# MAGIC   "logType": "auto_detected",
# MAGIC   "minutesAfterWakeup": 1,
# MAGIC   "minutesAsleep": 481,
# MAGIC   "minutesAwake": 59,
# MAGIC   "minutesToFallAsleep": 0,
# MAGIC   "startTime": "2023-11-03T22:39:00.000",
# MAGIC   "timeInBed": 540,
# MAGIC   "type": "stages`
# MAGIC ```

# COMMAND ----------

display(fitbit_sleep_log_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Example Question:
# MAGIC - What % of the time was I sleeping vs % of the time I was awake (for a given day, range of days, month, etc.)
# MAGIC
# MAGIC Calculate sleeping efficiency using **minutesAwake vs. minutesAsleep**

# COMMAND ----------

first_row = fitbit_sleep_log_df.collect()[0]

minutes_awake = first_row[0]['minutesAwake']
minutes_asleep = first_row[0]['minutesAsleep']

total_time = minutes_asleep + minutes_awake
percent_asleep = (minutes_asleep / total_time) * 100
percent_awake = (minutes_awake / total_time) * 100

print("Percent Asleep: {:.2f}%".format(percent_asleep))
print("Percent Awake: {:.2f}%".format(percent_awake))

# COMMAND ----------

# MAGIC %md
# MAGIC Plot it, show a simple stacked bar chart

# COMMAND ----------

# Initialize the plot
plt.figure(figsize=(6, 8))
plt.title('Sleeping Efficiency \U0001F634')
plt.ylabel('Percentage of Time')

# Plot the bars
bar1 = plt.bar(['Sleep'], [percent_asleep], color='tab:blue', label='Asleep')
bar2 = plt.bar(['Sleep'], [percent_awake], bottom=[percent_asleep], color='salmon', label='Awake')

# Get height of the bars
height1 = bar1[0].get_height()
height2 = bar2[0].get_height()

# Add labels on top of the bars with center alignment
plt.text(x=0, y=height1/2, s='{:.0f}%'.format(percent_asleep), ha='center', va='center')
plt.text(x=0, y=height1+height2/2, s='{:.0f}%'.format(percent_awake), ha='center', va='center')

# Show the chart
plt.legend(loc='upper center', bbox_to_anchor=[0.5, 1.15], ncol=2)
plt.show()

# COMMAND ----------

display(fitbit_daily_activity_df)

# COMMAND ----------

display(fitbit_user_profile_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Display Hevy data
# MAGIC One row = one workout
# MAGIC
# MAGIC 2 most important metrics:
# MAGIC - duration (how long training session)
# MAGIC - estimated_volume_kg (how much total weight lifted)

# COMMAND ----------

display(hevy_workouts_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC Show volume lifted. Compare workouts

# COMMAND ----------

workout_rows = hevy_workouts_df.take(2)

# Convert start and end times from strings to integers and calculate duration in minutes
workout1_duration_minutes = (int(workout_rows[0]['end_time']) - int(workout_rows[0]['start_time'])) / 60
workout2_duration_minutes = (int(workout_rows[1]['end_time']) - int(workout_rows[1]['start_time'])) / 60

workout1_volume = float(workout_rows[0]['estimated_volume_kg'])
workout2_volume = float(workout_rows[1]['estimated_volume_kg'])

# display these values in a 2x2 grid using matplotlib
workouts = ['Workout 1', 'Workout 2']
durations = [workout1_duration_minutes, workout2_duration_minutes]
volumes = [workout1_volume, workout2_volume]  # Make sure these are numeric
x = range(len(workouts))  # x-coordinates for the bars

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Ensure we only provide two colors for the two bars
colors = ['blue', 'green']

# Plotting Duration of Each Workout
axs[0, 0].bar(x, durations, color=colors)
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(workouts)
axs[0, 0].set_title('Duration of Each Workout (in minutes)')
axs[0, 0].set_ylabel('Duration (minutes)')

# Plotting Total Volume for Each Workout
axs[1, 0].bar(x, volumes, color=colors)
axs[1, 0].set_xticks(x)
axs[1, 0].set_xticklabels(workouts)
axs[1, 0].set_title('Total Volume of Each Workout (in kg)')
axs[1, 0].set_ylabel('Volume (kg)')

# Setting the other plots as empty/blank
axs[0, 1].axis('off')
axs[1, 1].axis('off')

# Add labels on top of the bars with center alignment
for i, v in enumerate(durations):
    axs[0, 0].text(i, v, f'{round(v)}', ha='center', va='bottom', fontweight='bold')
for i, v in enumerate(volumes):
    # Make sure to add a small offset to 'v' to position the label above the bar
    axs[1, 0].text(i, v, f'{round(v)}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Display Polar data
# MAGIC
# MAGIC one row = one exercise session (walking, cycling, running, etc.)
# MAGIC
# MAGIC Note: Polar has two apps (Polar Flow and Polar BEAT). As far as I can tell from experimenting, functionally they do the same thing and provide the same data

# COMMAND ----------

display(polar_exercises_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC Heart rate data is the most important.
# MAGIC
# MAGIC ```
# MAGIC "{'average': 82, 'maximum': 117}"
# MAGIC ```
# MAGIC
# MAGIC Goal to use HRMAX Training Zones 1-5, then can see training intensity of each exercise
# MAGIC
# MAGIC Display a graph of the average heart rate for each training zone

# COMMAND ----------

data = [
    (1, '{"average": 114}'),
    (2, '{"average": 133}'),
    (3, '{"average": 155}'),
    (4, '{"average": 171}'),
    (5, '{"average": 190}'),
]
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("heart_rate", StringType(), True)
])
polar_exercises_df = spark.createDataFrame(data, schema=schema)

# Parse the JSON and extract the average heart rate
schema = StructType([
    StructField("average", IntegerType(), True)
])
polar_exercises_df = polar_exercises_df.withColumn("heart_rate_json", from_json(col("heart_rate"), schema))

# Extract the average heart rate from the JSON structure
polar_exercises_df = polar_exercises_df.withColumn("average_heart_rate", col("heart_rate_json.average"))

# Define the training zones based on the average heart rate
zone1 = (polar_exercises_df["average_heart_rate"] < 120)
zone2 = (polar_exercises_df["average_heart_rate"] >= 120) & (polar_exercises_df["average_heart_rate"] < 140)
zone3 = (polar_exercises_df["average_heart_rate"] >= 140) & (polar_exercises_df["average_heart_rate"] < 160)
zone4 = (polar_exercises_df["average_heart_rate"] >= 160) & (polar_exercises_df["average_heart_rate"] < 180)
zone5 = (polar_exercises_df["average_heart_rate"] >= 180)

# Add new column to indicate the training zones for each row
polar_exercises_df = polar_exercises_df.withColumn("training_zone", 
        when(zone1, "Zone 1")
       .when(zone2, "Zone 2")
       .when(zone3, "Zone 3")
       .when(zone4, "Zone 4")
       .when(zone5, "Zone 5")
       .otherwise("Unknown"))

# Aggregate data by the training zone and calculate the average heart rate for each zone
zone_hr_avg = polar_exercises_df.groupBy("training_zone").agg(avg("average_heart_rate").alias("avg_heart_rate"))

# Convert Spark DataFrame to Pandas DataFrame
zone_hr_avg_pd = zone_hr_avg.toPandas()

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(zone_hr_avg_pd["training_zone"], zone_hr_avg_pd["avg_heart_rate"].round().astype(int), color='blue', alpha=0.7)
plt.title('Average Heart Rate for Each Training Zone')
plt.xlabel('Training Zones')
plt.ylabel('Average Heart Rate')

# Add labels inside the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Verify Kaggle Datasets
# MAGIC The dataset formats from Kaggle can vary - often either a single csv or multiple csvs
# MAGIC
# MAGIC The upload script for loading files into ADLS automatically merges each dataset into a single csv
# MAGIC
# MAGIC Make sure dataset columns/values line up properly

# COMMAND ----------

# MAGIC %md
# MAGIC ## Crossfit
# MAGIC source: https://www.kaggle.com/datasets/ulrikthygepedersen/crossfit-athletes

# COMMAND ----------

display(crossfit_athletes_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## NFL Combine Results (2000 - 2022)
# MAGIC source: https://www.kaggle.com/datasets/mitchellweg1/nfl-combine-results-dataset-2000-2022

# COMMAND ----------

display(nfl_combine_results_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC # Verify Manually Scraped Dataset

# COMMAND ----------

# MAGIC %md
# MAGIC ## World Athletics
# MAGIC source: https://mastersrankings.com/rankings/
# MAGIC
# MAGIC Verify values are showing correctly, especially for performance, athlete name, and age.

# COMMAND ----------

display(world_athletics_df.limit(20))

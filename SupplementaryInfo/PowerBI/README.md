# CSCI 622 Project - Brock

## How to Interact With the Dashboard
- Click on a day on the calendar. It will highlight the selected day, and display the corresponding metrics for heart rate training zone and sleep. The tooltip on the day shows workout notes.

> ![Dashboard Demo Day Selection](/SupplementaryInfo/screenshots/dashboard-demo-day-selection.gif)

# Getting Started With PowerBI
To run and view the PowerBI dashboard on your computer, follow the instructions below.

## View Dashboard Online
1. Visit https://brocg.github.io/athlete-performance-dashboard (works best in Chrome/Edge)
2. If prompted for login, use @ndus.edu credentials (might require agreeing to a prompt for free trial)

## View Dashboard Locally (using PowerBI)

1. Download [PowerBI Desktop](https://powerbi.microsoft.com/en-us/desktop/)
2. Open "HevyWorkoutsBI.pbix" file ([download here](https://drive.google.com/file/d/1MkpzdAuhd_52cgjENi1LC1JIHep5rx-5/view?usp=sharing), also in this repo)
3. The dashboard contains 2 visuals that rely on Python scripts and the matplotlib library (for making the graphs). Click "enable" visuals (you can review the code before enabling)
> ![Enable Script Visuals](/SupplementaryInfo/screenshots/enable-script-visuals.png)
> ![Review Script Visuals](/SupplementaryInfo/screenshots/review-script-visuals.png)
4. Ensure that Python is installed locally on your computer and available in your environment. Check "Detected Python home directory" under Files > Options and Settings > Options > Python Script Settings. Update the directory and/or install Python if needed.
> ![Enable Python](/SupplementaryInfo/screenshots/python-script-settings.png)
3. Ensure the 3 datasource files are pulling from this Azure Blob Service (https://samplestorepowerbi.blob.core.windows.net/f23-proj/). You can verify the container address by going to File > Options and Settings > Data Source Settings
> ![Review Script Visuals](/SupplementaryInfo/screenshots/data-source-settings.png)
4. Click "Refresh" on Ribbon, all data should load in : )
> ![Refresh Data](/SupplementaryInfo/screenshots/refresh-data.png)

For further customization, I recommend using the 3 files in "SupplementaryInfo/PowerBI/raw-datafiles" as your data sources (so it doesn't rely on the Azure Blob container). Then you have complete control to edit the data as you see fit. It'll require rejoining the three tables, and a few other tweaks, but should be doable.

The data provided in this repo is based on real data, but for the purpose of this example I added in more synthetic records to popualte the calendar. So you might notice some irregularities in the data upon closer inspection.

## Overall Functionality
Enjoy testing this out! It's a prototype dashboard, so open to any suggestions and feedback. 

### Browing calendar days to see stats
- Click on a day on the calendar. It will highlight the selected day, and display the corresponding metrics for heart rate training zone and sleep. The tooltip on the day shows workout notes.
> ![Dashboard Demo Day Selection](/SupplementaryInfo/screenshots/dashboard-demo-day-selection.gif)

### Browsing workout types to see aggregated stats
- Click on a workout type on the top bar of the calendar. It will highlight the selected workouts, and show a summary.
> ![Dashboard Demo Workout Type Selection](/SupplementaryInfo/screenshots/dashboard-demo-workout-type.gif)

### Some features I'd like to add on the next iteration:
This was my first time using PowerBI, so there's a lot left to be desired. Here's a few features I'd like to implement next.

- When you click on the PolarH10 Heart Rate Dates, this should tie back to the calendar and select the matching day automatically
- When selecting a workout, I want to see the specific details. Volume lifted, distance run, total duration, etc.
- Instead of just a number, use a histogram visual to see total hours of sleep, including a week-over-week summary, or last X days.

## Final Thoughts
Overall I'm impressed with PowerBI's functionality out of the box. I didn't realize by relying on custom Python scripts in PowerBI it'd make it much harder to share this file locally.

Moving forward, I think I'll continue to use Azure Data Bricks (ADB) to do verify and do transformations on the data, but then load the data into a database (instead of PowerBI). From there I might design a single page application using a library (i.e. React) and achieve similar visuals.

It was fun to experiment with PowerBI and excited to see how this evolves as I use it for logging training.
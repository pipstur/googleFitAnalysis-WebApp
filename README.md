# Google Fit Analysis Web App

This web application allows you to analyze and visualize data from Google Fit. Upload your Google Fit data in CSV format to generate plots and insights about your fitness activities. You can get this data from [here](https://takeout.google.com/?pli=1).  

It is a simple matter of:
- Requesting the data from Google about your Google fit application
- Waiting for the data to arrive (might take a long time)
- Then finding the "Daily Activity Metrics.csv" file (I've included mine if you want to just try it out). The file can be found inside the Takeout folder that you will get after google is ready with your info and then going into Fit/Daily activity metrics/Daily activity metrics.csv.

## Getting Started
1. **Go to** [this link](https://pipstur.github.io/googleFitAnalysis-WebApp/). The service is hosted using pythonanywhere and githubpages.
2. **Upload Data:**
    - Click the "Choose File" button to select your Google Fit data in CSV format.
    - Click the "Upload" button to upload the selected file.

3. **Analyze Plots:**
    - Use the "Fetch and analyze plots" button to generate plots based on the uploaded data.

4. **Explore Results:**
    - View the results and insights below the upload form.
    - Analyze distance plots and other fitness metrics.

## Available Plots

- **Distance Plot:** Visualizes distance covered over time.
- **Average Steps Plot:** Shows average steps over weeks of the year.
- **Heart Points vs Steps:** Compares heart points and step count.
- **Mean Steps by Day of Week:** Displays mean steps for each day of the week.
- **Mean Steps by Month:** Illustrates mean steps for each month.

## File Structure

- `index.html`: Main HTML file with the user interface.
- `script.js`: JavaScript file for handling file uploads and fetching/plots.
- `style.css`: CSS file for styling the page.
- `app.py`: Used for the backend code and handling of data.



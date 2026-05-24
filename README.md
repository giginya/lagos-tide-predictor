# Lagos Harbour Tide Predictor

This Streamlit app generates tide predictions for Lagos Harbour over a selected date and time range. It displays the full tide table, detected high waters, detected low waters, a tidal curve, and a downloadable CSV file.

## Requirements

- Python 3.9 or newer
- Internet access for first-time package installation
- The packages listed in `requirements.txt`

## Setup

From the project folder, install the required packages:

```bash
pip install -r requirements.txt
```

## Run The App

Start the Streamlit app from the project folder:

```bash
streamlit run app.py
```

Streamlit will show a local web address, usually:

```text
http://localhost:8501
```

Open that address in a browser.

## How To Use

1. Select the start date.
2. Select the start time.
3. Select the end date.
4. Select the end time.
5. Choose the prediction interval in minutes.
6. Click `Generate Prediction`.

The app will then show:

- `Tide Table`: all generated tide heights.
- `High Waters`: detected high water times and heights.
- `Low Waters`: detected low water times and heights.
- `Tidal Curve`: a line chart of tide height over time.
- `Download CSV`: a button to download the full tide table.

## Input Limits

To keep the app responsive for multiple users:

- The end date and time must be after the start date and time.
- The prediction range is limited to 366 days.
- The interval must be between 1 and 1440 minutes.
- A single request cannot generate more than 20,000 rows.

If a request is too large, increase the interval or shorten the date range.

## Recommended Settings

For normal daily tide tables, use:

- Range: 1 to 7 days
- Interval: 10 to 30 minutes

For longer reports, use a larger interval such as 30 or 60 minutes.

## Troubleshooting

If the app does not start, reinstall the requirements:

```bash
pip install -r requirements.txt
```

If the browser page does not open automatically, copy the local address shown by Streamlit and paste it into your browser.

If the app says the request is too large, reduce the date range or increase the interval.

## Notes

The prediction is based on the harmonic constituents implemented in `tide_engine.py`. Results should be reviewed by a qualified hydrographic authority before use in safety-critical marine operations.
QUICK USER GUIDE FOR THE NIGERIAN NAVY @ 70 LAGOS HARBOUR TIDE PREDICTOR APP
The Lagos Harbour Tide Predictor is a temporary web-based application developed by the National Hydrographic Agency (NHA) for the Operations Directorate to support its maritime activities during the Nigerian Navy @ 70 Celebrations.
The application provides:
•	Tide predictions
•	High and low water information
•	Tidal curves
•	Downloadable tide tables

Application Link
https://nn-lagos-tide.streamlit.app
Important Notice
•	This is a web application only.
•	No installation is required.
•	Access is through the web link above.
•	The application was developed solely for the Operations Directorate by NHA in support of the NN @ 70 International Fleet Review activities.
•	The application will be withdrawn after 15 June 2026.
How To Use
1. Enter Start Date and Time
In the field labelled: Start Date (YYYY-MM-DD HH:MM) enter the required start date and time using the format:
    YYYY-MM-DD HH:MM
Example:
    2026-05-10 06:00
Meaning:
•	Year: 2026
•	Month: 05
•	Day: 10
•	Time: 06:00 AM
2. Enter End Date and Time
In the field labelled: End Date (YYYY-MM-DD HH:MM) enter the required end date and time using the same format.
Example:
    2026-05-12 18:00
Important:
•	The End Date and Time must be later than the Start Date and Time.
3. Select Interval Minutes
The interval determines how frequently tide heights are calculated.
Examples:
Interval	Meaning
15	Prediction every 15 minutes
30	Prediction every 30 minutes
60	Prediction every 1 hour
Recommended:
•	10–15 minutes for operational use
•	30 minutes for general planning
•	60 minutes for longer reports
Smaller intervals produce:
•	more detailed tide tables
•	smoother tidal curves
•	larger datasets

4. Generate Prediction
Click:
Generate Prediction
The application will display:
•	Tide Table
•	High Waters
•	Low Waters
•	Tidal Curve
5. Download Results
Click:
Download CSV
to download the generated tide table.
Operational Limits
•	Maximum prediction range: 366 days
•	Maximum rows per request: 20,000
•	Interval range: 1–1440 minutes
If a request is too large:
•	shorten the prediction range
•	or increase the interval
Disclaimer:
This application is intended for operational support purposes only. Tide predictions do not exenorate the captain, watch keeper or crew of responsibility for the safety of the ship and her crew, especially in restricted waters or waters where underkeel clearance is considered critical.


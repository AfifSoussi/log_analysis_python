# Log Analysis Tool
This Python script reads a log file, analyzes endpoint performance, and detects potential regressions. It compares the duration of requests to a calculated average, identifying any instances where performance exceeds a given threshold (30%) and reports these as regressions. The script is designed to be flexible and easy to extend, with key functionality separated into distinct functions.

# Features
Log Parsing: Reads logs formatted as text files and processes them into dictionaries using the JSON module.

Endpoint Statistics: Tracks total duration, request counts, and regression times for each API endpoint.

Regression Detection: Detects regressions when request durations exceed 30% of the average for a given endpoint.

Tolerance Control: Regressions are only reported if they occur more than 5 minutes apart.

Delta Calculation: Outputs the exact number of seconds by which the request duration exceeded the average for that endpoint.

Scalable Design: The logic is separated into modular functions, making it easy to maintain and expand.
# How It Works
## Step 1: Log Parsing
The script reads the log file as plain text and treats each line as a JSON object. If the logs are not in standard JSON format (as specified in the task), they are treated as strings and manipulated accordingly. A function was added to transform the text into JSON format in memory and save it for easier processing.

## Step 2: Calculating Averages
Each API endpoint's total request duration and request count are tracked in a dictionary (endpoint_stats). For each log entry, the script updates the total duration and increments the request count. The average duration is calculated by dividing the total duration by the request count.

## Step 3: Detecting Regressions
If a log entry has a request duration more than 30% higher than the average for that endpoint, it is flagged as a regression. Regressions are only reported if the last one occurred more than 5 minutes prior (configurable via a tolerance parameter).

## Step 4: Reporting Results
For each regression, the script outputs:

* The endpoint name
* The timestamp when the regression occurred
* The delta, showing how many seconds the duration exceeded the average for that endpoint

# Run the script
### Requirements
Python 3.x
JSON module (included in Python standard library)
### Usage
Place the log file (logs.txt) in the input directory.

``` bash
python log_analysis.py
``` 
The script will output detected regressions to the console. You can also enable file saving by modifying the script as needed.

## File Structure
* input/logs.txt: Input log file containing performance data in text format.
* input/mini.txt: a sample from the logs for quicker testing in the early phase.
* log_analysis.py: The main script performing log parsing, regression detection, and reporting.
* README.md: This file, containing the description of the project and instructions for usage.

## Additional Notes
The initial exercise assumed the file was JSON, but it was formatted as text with no array definition or delimiter separation between entries. The script now handles this by manipulating the text and converting it to JSON for easier processing.
The main logic is broken into three functions, with controls added between steps to ensure null or empty values are handled properly. This makes the script easier to scale and maintain.
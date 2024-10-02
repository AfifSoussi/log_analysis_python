import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

logpath="./input/logs.txt"


def read_logs_to_json():
    # Check if the file exists
    if not os.path.isfile(logpath):
        print(f"Error: {logpath} does not exist.exiting now")
        sys.exit(1) 

    logs_text=open(logpath,'r').read()
    # Split the input text into individual log entries
    log_entries = logs_text.strip().split("\n")
    
    # Convert each log entry to a Python dictionary
    json_objects = []
    for entry in log_entries:
        # Convert the text into a dictionary
        entry_dict = json.loads(entry)
        json_objects.append(entry_dict)
    
    # uncomment to save the input file as a proper json
    #with open("input/logs.json", 'w') as json_file:
    #    json.dump(json_objects, json_file, indent=4)
    
    return json_objects


def find_regression(json_objects, tolerance=5, regression_threshold=0.3):
    # Store the rolling average and the regression times
    endpoint_stats = defaultdict(lambda: {'total_duration': 0, 'count': 0, 'regressions': [], 'deltas': []})

    # Process each log entry
    for log in json_objects:
        timestamp = datetime.strptime(log['TimeStamp'], "%Y-%m-%dT%H:%M:%S")
        endpoint = log['Endpoint']
        duration = log['Duration']
        
        # Update the average for this endpoint
        stats = endpoint_stats[endpoint] 
        if stats['count'] > 0:
            average_duration = stats['total_duration'] / stats['count']
        #first log for this endpoint
        else:
            average_duration = 0

        stats['total_duration'] += duration
        stats['count'] += 1
        # print (endpoint,duration,average_duration," delta = " ,int(duration - average_duration),"regression = ",average_duration * (1 + regression_threshold))        
        
        # Detect regression (30% above the previous average)
        if average_duration > 0 and duration > average_duration * (1 + regression_threshold):
            # Check if the regression is within the tolerance window, or it's the first
            if not stats['regressions'] or timestamp - stats['regressions'][-1] > timedelta(minutes=tolerance):
                stats['regressions'].append(timestamp)
                delta = duration - average_duration  # Calculate the delta
                stats['deltas'].append(delta)  # Store the delta for output later
    
    return endpoint_stats

def print_regressions(regressions):
    # Output the regressed endpoints and the approximate times
    for endpoint, data in regressions.items():
        if data['regressions']:
            print(f" =================== Endpoint: {endpoint} =========================")
            for i, regression_time in enumerate(data['regressions']):
                delta = data['deltas'][i]  # Retrieve the stored delta for each regression
                print(f"  Regressed at approximately: {regression_time.strftime('%Y-%m-%d %H:%M:%S')} for {delta:.2f} seconds above average")

def main():
    print("Starting the analysis")

    # Step 1: Read logs and ensure it's not None or empty
    logs = read_logs_to_json()
    if not logs:
        print("Error: No logs were read. Exiting.")
        return  # Exit if logs are None or empty

    # Step 2: Find regressions and ensure the result is valid
    regressions = find_regression(logs)
    if not regressions:
        print("Error: No regressions found or an issue occurred during analysis.")
        return  # Exit if regressions are None or empty

    # Step 3: Print regressions if valid data is available
    print_regressions(regressions)
    print(" ------- all done -------")


if __name__ == '__main__':
    main()
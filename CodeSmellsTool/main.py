import csv
import pandas as pd
import yaml

# Load the file with code metrics into a DataFrame
df = pd.read_csv("C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/datasets/Metric.csv")
df = df.head(50)  # Select the first 50 rows

# Load the thresholds from the YAML file
with open("C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/config.yaml", "r") as file:
    thresholds = yaml.safe_load(file)['thresholds']

# Create a list to store the results
results = []

# Compare the metrics with the thresholds
for index, row in df.iterrows():
    result_row = {'File': row['File']}

    if row['Lines of Code'] >= thresholds['lines_of_code']:
        result_row['Lines of Code'] = f"Threshold exceeded. Value: {row['Lines of Code']}"
    else:
        result_row['Lines of Code'] = row['Lines of Code']

    if row['Num Plays'] >= thresholds['num_plays']:
        result_row['Num Plays'] = f"Threshold exceeded. Value: {row['Num Plays']}"
    else:
        result_row['Num Plays'] = row['Num Plays']

    if row['Avg Play Size'] >= thresholds['avg_play_size']:
        result_row['Avg Play Size'] = f"Threshold exceeded. Value: {row['Avg Play Size']}"
    else:
        result_row['Avg Play Size'] = row['Avg Play Size']

    if row['Num Tasks'] >= thresholds['num_tasks']:
        result_row['Num Tasks'] = f"Threshold exceeded. Value: {row['Num Tasks']}"
    else:
        result_row['Num Tasks'] = row['Num Tasks']

    if row['Avg Task Size'] >= thresholds['avg_task_size']:
        result_row['Avg Task Size'] = f"Threshold exceeded. Value: {row['Avg Task Size']}"
    else:
        result_row['Avg Task Size'] = row['Avg Task Size']

    if row['Num Vars'] >= thresholds['num_vars']:
        result_row['Num Vars'] = f"Threshold exceeded. Value: {row['Num Vars']}"
    else:
        result_row['Num Vars'] = row['Num Vars']

    results.append(result_row)

# Define the CSV file path and name
csv_file = "result.csv"

# Write the results to a CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# Provide the download link
download_link = f"<a href='file://{csv_file}' download>Download Results</a>"
print(download_link)

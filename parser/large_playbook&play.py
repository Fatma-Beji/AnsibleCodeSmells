import csv
from ansiblemetrics.general.lines_code import LinesCode
from ansiblemetrics.metrics_extractor import extract_all
from ansiblemetrics.playbook.num_tasks import NumTasks
from ansiblemetrics.playbook.num_plays import NumPlays
from ansiblemetrics.playbook.avg_play_size import AvgPlaySize
from ansiblemetrics.playbook.avg_task_size import AvgTaskSize
from ansiblemetrics.playbook.avg_task_size import AvgTaskSize
from ansiblemetrics.general.lines_comment import LinesComment
import os


# Define the path to the CSV file containing filtered YAML file paths
csv_file = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Data/playbooks.csv"

# Define the output CSV file path for metrics
metrics_csv_file = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Data/metrics.csv"

# Initialize Ansible metrics variables
metrics = {
    "lines_of_code": 0,
    "num_plays": 0,
    "avg_play_size": 0,
    "num_tasks": 0,
    "avg_task_size": 0
}

# Create or open the CSV file for metrics in write mode
with open(metrics_csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    
    # Write header row to the metrics CSV file
    writer.writerow(["File", "Lines of Code", "Num Plays", "Avg Play Size", "Num Tasks", "Avg Task Size"])
    
    # Read the CSV file containing filtered YAML file paths
    with open(csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            file_path = row[4]  # Assuming the YAML file path is in the fifth column of the CSV
            
            # Modify the path format to use forward slashes and remove leading/trailing spaces
            file_path = file_path.replace("\\", "/").strip()
            
            # Load YAML data
            try:
                with open(file_path, "r") as f:
                    #print(file_path)
                    yaml_data = f.read()

                    if not yaml_data:  # Check if the file is empty
                        continue

                    # Calculate metrics
                    loc = LinesCode(yaml_data).count() + LinesComment(yaml_data).count()
                    metrics["lines_of_code"] = loc
                    metrics["num_plays"] = NumPlays(yaml_data).count()
                    metrics["avg_play_size"] = AvgPlaySize(yaml_data).count()
                    metrics["num_tasks"] = NumTasks(yaml_data).count()
                    metrics["avg_task_size"] = AvgTaskSize(yaml_data).count()

                    # Write metrics to the metrics CSV file
                    writer.writerow([file_path, metrics["lines_of_code"], metrics["num_plays"], metrics["avg_play_size"], metrics["num_tasks"], metrics["avg_task_size"]])

            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except PermissionError:
                print(f"Permission denied: {file_path}")
            except Exception as e:
                print(f"Error reading file: {file_path}. Error message: {str(e)}")

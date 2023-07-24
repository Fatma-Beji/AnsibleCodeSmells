import csv
import yaml
from collections import Counter

# Define the path to the CSV file containing the local URLs of the YAML files
csv_file = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Data/playbooks.csv"

# Define the output CSV file path for scores
output_file = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Data/score_co_struct.csv"

# Initialize Ansible metrics variables
scores = {
    "Strut_Cohesion_Inter_Plays": 0,
    "Strut_Cohesion_Intra_Plays": 0,
}

# Create or open the CSV file for scores in write mode
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write header row to the scores CSV file
    writer.writerow(["File", "Strut Cohesion Inter Plays", "Strut Cohesion Intra Plays"])

    # Read the CSV file containing the local URLs of the YAML files
    with open(csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            file_path = row[4]  

            # Modify the path format to use forward slashes and remove leading/trailing spaces
            file_path = file_path.replace("\\", "/").strip()
            
            # Load YAML data
            try:
                with open(file_path, "r") as f:
                    yaml_data = yaml.load(f, Loader=yaml.Loader)

                    if not yaml_data:  # Check if the file is empty
                        continue

                    tasks = []
                    for play in yaml_data:
                        if 'tasks' in play:
                            tasks.extend(play['tasks'])

                
                    tasks_s = yaml_data if isinstance(yaml_data, list) else []
                


                    def extract_keys(data):
                        keys = []
                        if isinstance(data, dict):
                            for key, value in data.items():
                                keys.append(key)
                                keys.extend(extract_keys(value))
                        elif isinstance(data, list):
                            for item in data:
                                keys.extend(extract_keys(item))
                        return keys

                    if '/tasks/' in file_path:  # Check if the file path contains "tasks" folder
                        # Calculate inter-plays cohesion score for files with only tasks
                        all_keys = []
                        for task in tasks_s:
                            all_keys.extend(extract_keys(task))
                        key_counts = Counter(all_keys)
                        common_keys = [key for key, count in key_counts.items() if count > 1]
                        sum_common_keys = len(common_keys)
                        iou_score = sum_common_keys / len(set(all_keys))
                        iou_score_inter_plays = iou_score / len(tasks_s) if len(tasks_s) > 0 else 0
                        print("iou_score_inter_plays:", iou_score_inter_plays)
                        scores["Strut_Cohesion_Inter_Plays"] = iou_score_inter_plays

                        # Set intra-plays cohesion score equal to inter-plays cohesion score
                        scores["Strut_Cohesion_Intra_Plays"] = iou_score_inter_plays

                    else:


                        total_iou_score = 0  
                        num_plays = 0  
                        # Iterate over each play
                        for play in yaml_data:
                            if 'tasks' in play:
                                # Extract tasks from the play
                                tasks = play['tasks']
                                # Collect all keys from each task
                                all_keys = []
                                for task in tasks:
                                    all_keys.extend(extract_keys(task))
                                # Count the occurrences of each key
                                key_counts = Counter(all_keys)
                                # Get the keys that appear in more than one task
                                common_keys = [key for key, count in key_counts.items() if count > 1]
                                # Calculate the sum of common keys
                                sum_common_keys = len(common_keys)
                                # Calculate the intersection-over-union (IoU) score
                                iou_score = sum_common_keys / len(set(all_keys))
                                # Total score divided by num tasks
                                iou_tasks = iou_score / len(tasks) if len(tasks) > 0 else 0
                                # Print the total number of keys
                                total_keys = len(set(all_keys))
                                # Update the total IoU score and increment the number of plays
                                total_iou_score += iou_tasks
                                num_plays += 1
                                # Print a separator
                                print('-' * 20)
                        # Calculate the average IoU score
                        iou_score_intra_plays = total_iou_score / num_plays if num_plays > 0 else 0
                        # Print the average IoU score
                        print(f"iou_score_intra_plays: {iou_score_intra_plays}")
                        # Update the intra-plays score
                        scores["Strut_Cohesion_Intra_Plays"] = iou_score_intra_plays
                    
                    # Write metrics to the CSV file
                    writer.writerow([file_path, scores["Strut_Cohesion_Inter_Plays"], scores["Strut_Cohesion_Intra_Plays"]])
                        
            except Exception as e:
                print(f"Error reading file: {file_path}. Error message: {str(e)}")

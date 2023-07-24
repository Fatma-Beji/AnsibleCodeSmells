import os
import csv

# Path to the parent directory containing the owner folders
parent_directory = 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/projects'

# Path to the CSV file to store the result
csv_file_path = 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Annotation/resu.csv'

# Excluded directories
excluded_dirs = ['group_vars', 'host_vars', 'vars', 'data', 'files', 'meta', 'defaults']

# Set to store unique file paths
unique_files = set()

# Open the CSV file for writing
with open(csv_file_path, 'a', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Owner', 'Repo', 'Files Number', 'YAML Files Number', 'File URL'])

    # Iterate over the owner folders
    for owner_folder in os.listdir(parent_directory):
        owner_path = os.path.join(parent_directory, owner_folder)

        # Check if the item is a directory
        if os.path.isdir(owner_path):
            total_file_count = 0  # Total number of files for the project
            yaml_count = 0  # Total number of YAML files for the project
            yaml_urls = []  # List to store YAML file URLs

            # Iterate over all subdirectories recursively
            for root, dirs, files in os.walk(owner_path):
                # Exclude specific directories
                dirs[:] = [d for d in dirs if d not in excluded_dirs]

                # Check if the current folder is playbooks, tasks, or roles
                if os.path.basename(root) in ['playbooks', 'tasks', 'roles']:
                    # Iterate over the files in the folder
                    for file in files:
                        if 'test' not in file and 'var' not in file:  # Exclude files with 'test' or 'var' in their names
                            file_path = os.path.join(root, file)
                            total_file_count += 1

                            # Check if the file is a YAML file
                            if file.lower().endswith(('.yaml', '.yml')):
                                yaml_count += 1

                                # Check if the file has already been encountered
                                if file_path not in unique_files:
                                    unique_files.add(file_path)
                                    yaml_urls.append(file_path)

            # Write the final row for each URL separately
            for url in yaml_urls:
                writer.writerow([owner_folder, '', total_file_count, yaml_count, url])

print("Result saved in", csv_file_path)

import csv
from git import Git
import os

# Specify the path to your CSV file
csv_projects = 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/repos.csv'

# Read the dataset from the CSV file
dataset = []
with open(csv_projects, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        dataset.append(row)

# Specify the directory where you want to clone the projects
clone_directory = 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/projects'

# Iterate over the dataset and clone each project
for project in dataset:
    path = project['path']

    # Extract the owner and repo names from the combined path
    owner, repo = path.split('/')

    # Construct the clone URL for the project
    clone_url = f"https://github.com/{owner}/{repo}.git"

    # Construct the clone path
    clone_path = f"{clone_directory}/{owner}/{repo}"
    clone_path = clone_path.replace('\\', '/')  # Replace backslashes with forward slashes

    # Check if the clone directory already exists
    if not os.path.exists(clone_path) or os.listdir(clone_path) == []:
        # Create intermediate directories if they don't exist
        os.makedirs(clone_path, exist_ok=True)

        # Clone the project using GitPython's Git.clone()
        g = Git()
        g.clone(clone_url, clone_path)
        print(f"Project {owner}/{repo} cloned successfully.")
    else:
        print(f"Project {owner}/{repo} already exists. Skipping cloning.")

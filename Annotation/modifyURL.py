import csv
from urllib.parse import urlparse, urlunparse
import requests


# Function to check if a URL is accessible
def is_url_accessible(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
# Function to modify the path
def modify_path(path):
    parsed_url = urlparse(path)
    path_parts = path.split('/')
    print(path_parts)

    # Add 'blob' after owner and repo name
    path_parts.insert(5, 'blob')

    # Check if branch 'main' is accessible
    path_parts.insert(6, 'master')
    modified_path_main = '/'.join(path_parts)
    if is_url_accessible(modified_path_main):
        return modified_path_main
    else:
        path_parts = modified_path_main.split('/')
        #print(path_parts)
        path_parts.pop(6)
        #print(path_parts)

     # Add branch 'master' and check accessibility
    path_parts.insert(6, 'master')
    modified_path_master = '/'.join(path_parts)
    if is_url_accessible(modified_path_master):
        return modified_path_master
    else:
        path_parts = modified_path_main.split('/')
        #print(path_parts)
        path_parts.pop(6)
        #print(path_parts)

    # # Add branch 'develop' and check accessibility
    # path_parts.insert(6, 'develop')
    # modified_path_master = '/'.join(path_parts)
    # if is_url_accessible(modified_path_master):
    #     return modified_path_master
    # else:
    #     path_parts = modified_path_main.split('/')
    #     print(path_parts)
    #     path_parts.pop(6)
    #     print(path_parts)

# Read the CSV file and modify the paths
rows = []
with open('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Annotation/sample_.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        old_path = row[1]  # Assuming the path is in the first column
        new_path = modify_path(old_path)
        row[1] = new_path  # Update the path in the row
        rows.append(row)
        #print(new_path)  # You can save the modified path or perform further operations

# Save the modified paths in a new CSV file
with open('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Annotation/a.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Modified paths saved ")
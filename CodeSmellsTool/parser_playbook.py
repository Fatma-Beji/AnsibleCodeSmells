from detect_large_playbook import calculate_metrics_playbook  
from detect_large_play import calculate_metrics_play
from detect_large_task import calculate_metrics_task
from high_coupling import high_coupling
from duplicate_code import duplicate_code
#from include_vars import detect_unnecessary_include_vars
from set_fact import set_fact
from overriding_facts import overriding_facts
from unecessary_abs import unecessary_abs
from unnamed_paly import unnamed_play
from sem_cohesion import calculate_similarity
from unamed_play import unnamed_play
from itertools import zip_longest

import pandas as pd
import csv
import json
import yaml

def read_specific_values():
    specific_values = {}
    with open('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/CodeSmellsTool/thresholds.csv', 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            key, value = row[0], int(row[1])
            specific_values[key] = value
    return specific_values

def count_tasks_in_play(play):
    count = 0
    if 'tasks' in play:
        tasks = play['tasks']
        for task in tasks:
            if 'block' in task:
                count += len(task['block'])
            else:
                count += 1
    elif 'block' in play:
        count += len(play['block'])
    return count

def mainn(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        playbook = yaml.safe_load(f)
    
    # Vérifiez si le playbook est une liste de tâches
    is_task_only_playbook = isinstance(playbook, list) and all(isinstance(task, dict) and 'hosts' not in task and 'tasks' not in task for task in playbook)
    
    metrics_playbook = calculate_metrics_playbook(yaml_file_path)

    metrics_play = None

    if not is_task_only_playbook:
        metrics_play = calculate_metrics_play(yaml_file_path)
   
    metrics_task = calculate_metrics_task(yaml_file_path)
    metrics_high_coupling = high_coupling(yaml_file_path)
    duplicated_code = duplicate_code(yaml_file_path)
    
    unecessary_set_fact = set_fact(yaml_file_path)
    overriding_fact = overriding_facts(yaml_file_path)
    unecessary_abst = unecessary_abs(yaml_file_path)
    similarity = calculate_similarity(yaml_file_path)

    main_metrics = {
        'playbook_metrics': metrics_playbook,
        'high_coupling_metrics': metrics_high_coupling,
        'similarity': similarity,
        'duplicated_code': duplicated_code,
        'unecessary_set_fact': unecessary_set_fact,
        'overriding_facts': overriding_fact,
        'unecessary_abstraction': unecessary_abst,
        'plays': []
    }
    
    if metrics_play:
   
        task_counts = [count_tasks_in_play(play) for play in playbook]

        # Deuxième lecture pour associer les métriques
        tasks_by_play_id = {}
        for task in metrics_task:
            play_id = task.get('play_id')
            if play_id not in tasks_by_play_id:
                tasks_by_play_id[play_id] = []
            tasks_by_play_id[play_id].append(task)
        
        for play in metrics_play['Plays']:
            play_id = play.get('play_id')
            tasks_for_this_play = tasks_by_play_id.get(play_id, [])
            
            is_unnamed = unnamed_play(play.get('Play_name', None))
            
            play_entry = {
                'play_metrics': play,
                'unnamed_play': is_unnamed,
                'task_metrics': tasks_for_this_play 
            }
            main_metrics['plays'].append(play_entry)

    else:
        # Cas où le playbook ne contient que des tâches, sans plays
        play_entry = {
            'play_metrics': None,
            'unnamed_play': None,
            'task_metrics': metrics_task
        }
        main_metrics['plays'].append(play_entry)

            
    with open('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/CodeSmellsTool/tool.json', 'w') as f:
        json.dump(main_metrics, f, indent=4)
        
    return main_metrics

        
yaml_file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl3.yaml"
metrics_playbook = mainn(yaml_file_path)
if __name__ == "__main__":
    if metrics_playbook:
        print(metrics_playbook)

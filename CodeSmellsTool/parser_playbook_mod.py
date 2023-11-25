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


def read_yaml_file_paths(csv_file_path):
    with open(csv_file_path, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)  # Passer la première ligne (l'en-tête)
        return [row[0] for row in csvreader if row and row[0].strip()]

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

def mainn(yaml_file_path, csvwriter):
    if not yaml_file_path.strip():  
        print("Chemin du fichier YAML vide, ignoré.")
        return None

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

        
    return main_metrics

def write_metrics_to_csv(metrics, csvwriter, yaml_file_path):
    # Écrire les métriques du playbook
    csvwriter.writerow([
        yaml_file_path,  
        '',  # Play Name est vide
        '',  # Task Name est vide
        metrics['playbook_metrics'].get('LOC_playbook', 'NA'),
        metrics['playbook_metrics'].get('num_plays', 'NA'),
        metrics['playbook_metrics'].get('num_tasks_playbook', 'NA'),
        metrics['playbook_metrics'].get('avg_task_playbook', 'NA'),
        metrics['high_coupling_metrics'].get('Num_Imports', 'NA'),
        metrics['high_coupling_metrics'].get('Num_Roles', 'NA'),
        metrics.get('similarity', 'Na'),
        '', '', '', '', '', '', ''
    ])
    print( metrics.get('similarity', 'Na'))
    for play in metrics['plays']:
        # Si les métriques du play sont présentes
        if play['play_metrics']:
            csvwriter.writerow([
                '',  # La colonne du playbook est vide
                play['play_metrics'].get('Play_name', 'Unknown'),
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                play['play_metrics'].get('LOC_play', 'NA'),
                play['play_metrics'].get('num_tasks_play', 'NA'),
                play['play_metrics'].get('avg_task_play', 'NA'),
                play['play_metrics'].get('special_chars', 'NA'),
                '', '', ''
            ])
        
        # Écrire les métriques des tâches pour ce play (ou pour le playbook si play_metrics est None)
        for task in play['task_metrics']:
            csvwriter.writerow([
                '', '',  # Les colonnes du playbook et du play sont vides
                task.get('task_name', 'Unknown'),
                '', '', '', '', '', '', '', '', '', '', '',
                task.get('LOC_task', 'NA'),
                task.get('task_name_len', 'NA'),
                task.get('special_chars', 'NA'),
            ])
        
if __name__ == "__main__":
    # Lire les chemins des fichiers YAML depuis le fichier CSV
    yaml_file_paths = read_yaml_file_paths('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Model/sorted_paths.csv')
    
    with open('metrics.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Playbook Name', 'Play Name', 'Task Name', 'LOC_playbook', 'num_plays', 'num_tasks_playbook', 'avg_task_playbook', 'Num_Imports' , 'Num_Roles' , 'similarity' , 'LOC_play' , 'num_tasks_play' , 'avg_task_play', 'special_chars_play', 'LOC_task', 'task_name_len', 'special_chars_task'])
        
        for yaml_file_path in yaml_file_paths:
            metrics_playbook = mainn(yaml_file_path, csvwriter)
            if metrics_playbook:
                write_metrics_to_csv(metrics_playbook, csvwriter,yaml_file_path)
                print(f"Metrics for {yaml_file_path} have been written.")
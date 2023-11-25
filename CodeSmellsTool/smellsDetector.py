
from parser_playbook import mainn
import json
import csv
import pandas as pd

def read_thresholds():
    thresholds = {}
    with open('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/CodeSmellsTool/thresholds.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # sauter l'en-tête
        for row in reader:
            if len(row) < 2:
                print(f"Ligne ignorée car elle est incomplète : {row}")
                continue
            key, value = row[0], float(row[1])  
            thresholds[key] = value
    return thresholds


def assess_code_smells(metrics, thresholds):
    result = {
        'playbook': {
            'metrics': {},
            'plays': []
        }
    }
    
    # Niveau Playbook
    playbook_metrics = metrics.get('playbook_metrics', {})

    if any(playbook_metrics.get(key, 0) > thresholds.get(key, 0) for key in ['LOC_playbook', 'num_plays', 'avg_play_size', 'num_tasks_playbook']):
        result['playbook']['metrics']['large_playbook'] = 1
    else:
        result['playbook']['metrics']['large_playbook'] = 0
    
    if (
    (playbook_metrics.get('LOC_playbook', 0) > thresholds.get('LOC_playbook', 0) and playbook_metrics.get('num_plays', 0) > thresholds.get('num_plays', 0)) or
    (playbook_metrics.get('LOC_playbook', 0) > thresholds.get('LOC_playbook', 0) and playbook_metrics.get('num_tasks_playbook', 0) > thresholds.get('num_tasks_playbook', 0)) or
    playbook_metrics.get('Num_Imports', 0) > thresholds.get('Num_Imports', 0) or
    playbook_metrics.get('Num_Roles', 0) > thresholds.get('num_roles', 0)
    ):
        result['playbook']['metrics']['complex_playbook'] = 1

    else:
        result['playbook']['metrics']['complex_playbook'] = 0

    if (
    (playbook_metrics.get('LOC_playbook', 0) > thresholds.get('LOC_playbook', 0) and playbook_metrics.get('num_plays', 0) > thresholds.get('num_plays', 0)) 
    ):
        result['playbook']['metrics']['insufficient_modularization'] = 1
    else:
        result['playbook']['metrics']['insufficient_modularization'] = 0

    if any(playbook_metrics.get(key, 0) > thresholds.get(key, 0) for key in ['Num_Imports', 'Num_Roles']):
        result['playbook']['metrics']['high_coupling'] = 1
    else:
        result['playbook']['metrics']['high_coupling'] = 0
            
    if metrics.get('similarity', 0) < thresholds.get('similarity', 0):
        result['playbook']['metrics']['incohesive_playbook'] = 1
    else:
        result['playbook']['metrics']['incohesive_playbook'] = 0

    for key in ['duplicated_code', 'unecessary_set_fact', 'overriding_facts', 'unecessary_abstraction']:
        if metrics.get(key, 0) == 1:
            result['playbook']['metrics'][key] = 1
        else:
            result['playbook']['metrics'][key] = 0

    # Niveau Play
    if 'plays' in metrics:
        
        for play in metrics['plays']:
            if play.get('play_metrics', {}) != None:
        
                # Si play_metrics n'est pas None, alors on continue comme avant
                play_result = {
                    'exist_play': 1,
                    'play_name': play.get('play_metrics', {}).get('Play_name', 'Unknown'),
                    'metrics': {},
                    'tasks': []
                }
                    
                if any(play_result.get(key, 0) > thresholds.get(key, 0) for key in ['LOC_play', 'num_tasks_play', 'avg_task_size']):
                    play_result['metrics']['large_play'] = 1
                else:
                    play_result['metrics']['large_play'] = 0
            
                if play.get('unnamed_play', 0) == 1:
                    play_result['metrics']['unnamed_play'] = 1
                else:
                    play_result['metrics']['unnamed_play'] = 0

            
                if 'task_metrics' in play:
                    for task in play['task_metrics']:
                        task_result = {
                            'task_name': task.get('task_name', 'Unknown'),
                            'metrics': {}
                        }
            
                        if task.get('LOC_task', 0) > thresholds.get('LOC_task', 0):
                            task_result['metrics']['large_task'] = 1
                        else:
                            task_result['metrics']['large_task'] = 0

                        if task.get('task_name_len', 0) > thresholds.get('task_name_len', 0):
                            task_result['metrics']['long_task_name'] = 1
                        else:
                            task_result['metrics']['long_task_name'] = 0

                        if task.get('special_chars', 0) > thresholds.get('special_chars', 0) or play.get('special_chars', 0) > thresholds.get('special_chars', 0) :
                            result['playbook']['metrics']['inconsistent_naming_convention'] = 1
                        else:
                            result['playbook']['metrics']['inconsistent_naming_convention'] = 0

                        play_result['tasks'].append(task_result)
                   
            else:
               
                play_result = {
                    'exist_play': 0,
                    'tasks': []
                }
                if 'task_metrics' in play:
                    for task in play['task_metrics']:
                        task_result = {
                            'task_name': task.get('task_name', 'Unknown'),
                            'metrics': {}
                        }
                        
                        if task.get('LOC_task', 0) > thresholds.get('LOC_task', 0):
                            task_result['metrics']['large_task'] = 1
                        else:
                            task_result['metrics']['large_task'] = 0

                        if task.get('task_name_len', 0) > thresholds.get('task_name_len', 0):
                            task_result['metrics']['long_task_name'] = 1
                        else:
                            task_result['metrics']['long_task_name'] = 0

                        if task.get('special_chars', 0) > thresholds.get('special_chars', 0):
                            result['playbook']['metrics']['inconsistent_naming_convention'] = 1
                        else:
                            result['playbook']['metrics']['inconsistent_naming_convention'] = 0  

                        play_result['tasks'].append(task_result)
            result['playbook']['plays'].append(play_result)
    return result

def write_results_to_csv(all_results, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Playbook Path', 'Play Name', 'Task Name', 'duplicated code', 'complex playbook', 'high playbook coupling', 'Large Playbook', 'Unnecessary set_fact', 'Overriding facts', 'Incohesive Playbook', 'Unecessary Abstraction', 'Insufficient Modularization', 'Inconsistent Naming Convention', 'Large Play', 'Unnamed Play', 'Large Task', 'Long Task Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Écrire les en-têtes des colonnes

        for playbook_path, playbook_data in all_results.items():
            writer.writerow({
                'Playbook Path': playbook_path, 
                'Play Name': '', 
                'Task Name': '', 
                'duplicated code':playbook_data['playbook']['metrics'].get('duplicated_code', ''), 
                'complex playbook':playbook_data['playbook']['metrics'].get('complex_playbook', ''), 
                'high playbook coupling':playbook_data['playbook']['metrics'].get('high_coupling', ''),
                'Large Playbook':playbook_data['playbook']['metrics'].get('large_playbook', ''),
                'Unnecessary set_fact':playbook_data['playbook']['metrics'].get('unecessary_set_fact', ''), 
                'Overriding facts':playbook_data['playbook']['metrics'].get('overriding_facts', ''), 
                'Incohesive Playbook':playbook_data['playbook']['metrics'].get('incohesive_playbook', ''), 
                'Unecessary Abstraction':playbook_data['playbook']['metrics'].get('unecessary_abstraction', ''), 
                'Insufficient Modularization':playbook_data['playbook']['metrics'].get('insufficient_modularization', ''), 
                'Inconsistent Naming Convention':playbook_data['playbook']['metrics'].get('inconsistent_naming_convention', ''), 
                'Large Play':'', 
                'Unnamed Play':'', 
                'Large Task':'', 
                'Long Task Name':''})


            for play in playbook_data['playbook'].get('plays', []):
                
                if play.get('exist_play', '') == 1:
                    
                    writer.writerow({
                        'Playbook Path': '', 
                        'Play Name': play.get('play_name', 'Unknown'), 
                        'Task Name': '', 
                        'duplicated code':'', 
                        'complex playbook':'', 
                        'high playbook coupling':'', 
                        'Large Playbook':'', 
                        'Unnecessary set_fact':'', 
                        'Overriding facts':'', 
                        'Incohesive Playbook':'', 
                        'Unecessary Abstraction':'', 
                        'Insufficient Modularization':'', 
                        'Inconsistent Naming Convention':'', 
                        'Large Play':play.get('metrics', {}).get('large_play', ''), 
                        'Unnamed Play':play.get('metrics', {}).get('unnamed_play', ''), 
                        'Large Task':'', 
                        'Long Task Name':''})

                    for task in play.get('tasks', []):
                        
                        writer.writerow({
                            'Playbook Path': '', 
                            'Play Name': '', 
                            'Task Name': task.get('task_name', 'Unknown'), 
                            'duplicated code':'', 
                            'complex playbook':'', 
                            'high playbook coupling':'', 
                            'Large Playbook':'', 
                            'Unnecessary set_fact':'', 
                            'Overriding facts':'', 
                            'Incohesive Playbook':'', 
                            'Unecessary Abstraction':'', 
                            'Insufficient Modularization':'', 
                            'Inconsistent Naming Convention':'', 
                            'Large Play':'', 
                            'Unnamed Play':'', 
                            'Large Task':task.get('metrics', {}).get('large_task', ''),  
                            'Long Task Name':task.get('metrics', {}).get('long_task_name', '')})
                else:
                    
                    for task in play.get('tasks', []):
                        
                        writer.writerow({
                            'Playbook Path': '', 
                            'Play Name': '', 
                            'Task Name': task.get('task_name', 'Unknown'), 
                            'duplicated code':'', 
                            'complex playbook':'', 
                            'high playbook coupling':'', 
                            'Large Playbook':'', 
                            'Unnecessary set_fact':'', 
                            'Overriding facts':'', 
                            'Incohesive Playbook':'', 
                            'Unecessary Abstraction':'', 
                            'Insufficient Modularization':'', 
                            'Inconsistent Naming Convention':'', 
                            'Large Play':'', 
                            'Unnamed Play':'', 
                            'Large Task':task.get('metrics', {}).get('large_task', ''),  
                            'Long Task Name':task.get('metrics', {}).get('long_task_name', '')})
                        
def execute_for_single_file(yaml_file_path):
    # Dictionnaire pour stocker les métriques
    all_metrics = {}
    # Dictionnaire pour stocker les résultats des "code smells"
    all_results = {}
    # Lire les seuils à partir du fichier CSV
    thresholds = read_thresholds()
    
    try:
        print(f"Traitement du fichier {yaml_file_path}...")
        # Obtenir les métriques pour le playbook courant
        metrics = mainn(yaml_file_path)
        # Ajouter les métriques au dictionnaire
        all_metrics[yaml_file_path] = metrics
        # Évaluer les "code smells" pour le playbook courant
        result = assess_code_smells(metrics, thresholds)
        # Ajouter les résultats au dictionnaire
        all_results[yaml_file_path] = result
    except Exception as e:
        print(f"Une erreur est survenue lors du traitement du fichier {yaml_file_path}: {e}")

    write_results_to_csv(all_results, 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/CodeSmellsTool/report.csv')
    write_results_to_txt(all_results, 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/CodeSmellsTool/report.txt')
    print("Les résultats de la détection des 'code smells' ont été enregistrés avec succès!")

def write_results_to_txt(all_results, file_path):
    with open(file_path, 'w') as txtfile:
        for playbook_path, playbook_data in all_results.items():
            txtfile.write(f"Code smells détectés pour le playbook {playbook_path}:\n")
            
            playbook_smells = [k for k, v in playbook_data['playbook']['metrics'].items() if v == 1]
            if playbook_smells:
                for smell in playbook_smells:
                    txtfile.write(f"- {smell}\n")
            else:
                txtfile.write("Aucun code smell détecté.\n")

            for play in playbook_data['playbook'].get('plays', []):
                play_smells = [k for k, v in play.get('metrics', {}).items() if v == 1]

                if play.get('exist_play', '') == 1:
                    txtfile.write(f"\nPour le play {play.get('play_name', 'Unknown')}:\n")

                    if play_smells:
                        for smell in play_smells:
                            txtfile.write(f"- {smell}\n")
                    else:
                        txtfile.write("Aucun code smell détecté pour ce play.\n")

                    for task in play.get('tasks', []):
                        task_smells = [k for k, v in task.get('metrics', {}).items() if v == 1]
                        
                        txtfile.write(f"\n\tPour la task {task.get('task_name', 'Unknown')}:\n")
                        if task_smells:
                            for smell in task_smells:
                                txtfile.write(f"\t- {smell}\n")
                        else:
                            txtfile.write("\tAucun code smell détecté pour cette task.\n")
                else:
                    for task in play.get('tasks', []):
                        task_smells = [k for k, v in task.get('metrics', {}).items() if v == 1]
                        
                        txtfile.write(f"\n\tPour la task {task.get('task_name', 'Unknown')}:\n")
                        if task_smells:
                            for smell in task_smells:
                                txtfile.write(f"\t- {smell}\n")
                        else:
                            txtfile.write("\tAucun code smell détecté pour cette task.\n")
            
            txtfile.write("\n\n")


if __name__ == "__main__":
    # Demande à l'utilisateur d'entrer le chemin du fichier YAML
    yaml_file_path = input("Entrez le chemin d'accès du fichier YAML : ")
    execute_for_single_file(yaml_file_path)
    


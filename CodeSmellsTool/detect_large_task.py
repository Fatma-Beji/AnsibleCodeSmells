import yaml
import pandas as pd
import re
import regex as re

def compter_lignes_dans_task(task):
    return yaml.dump([task]).count('\n')

def compter_caracteres_speciaux(chaine):
    return len(re.findall(r'[^\p{L}\p{N}\s]', chaine))

def analyser_tasks(tasks, metrics, play_id):
    for task in tasks:
        # Si c'est un block, analyser les tasks à l'intérieur

        if 'name':
            # Sinon, c'est une tâche standard
            lignes = compter_lignes_dans_task(task)
            nom = task.get('name', 'Unknown')
            metrics.append({
                'play_id': play_id,
                'task_name': nom, 
                'LOC_task': lignes, 
                'task_name_len': 0 if nom == 'Unknown' else len(nom),  
                'special_chars': compter_caracteres_speciaux(nom) if nom else 0
            })
        if 'block' in task:
            analyser_tasks(task['block'], metrics, play_id)

def analyser_play(play, metrics, play_id):
    if 'block' in play:
        analyser_tasks(play['block'], metrics, play_id)

    elif 'tasks' in play:
        for task in play['tasks']:
            if 'block' in task:  # Si c'est un block, analyser les tasks à l'intérieur
                analyser_tasks(task['block'], metrics, play_id)
            else:  # Sinon, c'est une tâche standard
                analyser_tasks([task], metrics, play_id)

def calculate_metrics_task(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        playbook = yaml.safe_load(f)

    all_metrics = []

    # Si le playbook est une liste
    if isinstance(playbook, list):
        has_plays = False  # Un indicateur pour vérifier si le playbook contient des plays
        
        # Vérifie si le playbook contient des plays
        for play_or_task in playbook:
            if isinstance(play_or_task, dict):
                if "tasks" in play_or_task or "hosts" in play_or_task:
                    has_plays = True
                    break  # Arrête la boucle dès qu'un play est trouvé

        if has_plays:
            #print("y a plays")
            play_id = 0
            for play in playbook:
                analyser_play(play, all_metrics, play_id)
                play_id += 1
                #print(play)
        else:
            #print("pas de plays")
            analyser_tasks(playbook, all_metrics, play_id=-1)

    return all_metrics

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl copy.yaml"  # Remplacez par le chemin de votre playbook
metrics = calculate_metrics_task(file_path)

if __name__ == '__main__':
    if metrics:
        df = pd.DataFrame(metrics)
        print(df)
    else:
        print('Pas de métriques disponibles.')

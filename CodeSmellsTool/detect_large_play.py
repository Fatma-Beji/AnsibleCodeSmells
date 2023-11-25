import yaml
import pandas as pd
import re

def compter_caracteres_speciaux(chaine):
    return len(re.findall(r'[^\w\s]', chaine))

def compter_tasks_dans_play(play):
    nombre_tasks = 0
    tasks = play.get('tasks', [])
    nombre_tasks += len(tasks)
    
    # Trouver des blocks dans le play
    if 'block' in play:
        block_tasks = play['block']
        nombre_tasks += len(block_tasks)

    #print(nombre_tasks)
    return nombre_tasks


def est_un_play(element):
    return 'hosts' in element or 'tasks' in element 

def calculate_metrics_play(yaml_file_path):
    metrics = {}
    plays_metrics = []

    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        playbook = yaml.safe_load(f)

    if not playbook or not isinstance(playbook, list):
        print(f"Erreur : Le fichier {yaml_file_path} n'est pas un playbook valide.")
        return None

    play_id = 0
    for element in playbook:
        if est_un_play(element):
            nom_play = element.get('name') 
            if not nom_play:
                nom_play = 'unknown'
            nombre_tasks = compter_tasks_dans_play(element)
            lignes_play = yaml.dump([element]).count('\n')
            avg_task_size = lignes_play / nombre_tasks if nombre_tasks > 0 else 0
            special_chars_count = compter_caracteres_speciaux(nom_play) if nom_play else 0
            
            plays_metrics.append({
                'play_id': play_id,
                'Play_name': nom_play,
                'LOC_play': lignes_play,
                'num_tasks_play': nombre_tasks,
                'avg_task_play': avg_task_size,
                'special_chars': special_chars_count  # Ajouter la nouvelle métrique ici
            })
            play_id += 1

    metrics['Plays'] = plays_metrics
    return metrics

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"  # Remplacez par le chemin de votre playbook
metrics = calculate_metrics_play(file_path)

if __name__ == '__main__':
    if metrics:
        for i, play_metrics in enumerate(metrics['Plays']):
            df = pd.DataFrame([play_metrics])
            print(f"DataFrame pour le Play {i + 1}:")
            print(df)
    else:
        print('Pas de métriques disponibles.')

from ansiblemetrics.general.lines_code import LinesCode
from ansiblemetrics.playbook.num_tasks import NumTasks
from ansiblemetrics.playbook.num_plays import NumPlays
from ansiblemetrics.playbook.avg_play_size import AvgPlaySize
from ansiblemetrics.playbook.avg_task_size import AvgTaskSize
from ansiblemetrics.general.lines_comment import LinesComment
import pandas as pd

def calculate_metrics_playbook(yaml_file_path):
    metrics = {}
    try:
        with open(yaml_file_path, 'r') as f:
            yaml_data = f.read()
        
        if not yaml_data:
            return None

        # Calculer les métriques
        metrics['LOC_playbook'] = LinesCode(yaml_data).count() + LinesComment(yaml_data).count()
        metrics['num_plays'] = NumPlays(yaml_data).count()
        metrics['avg_play_size'] = AvgPlaySize(yaml_data).count()
        metrics['num_tasks_playbook'] = NumTasks(yaml_data).count()
        metrics['avg_task_playbook'] = AvgTaskSize(yaml_data).count()
        
        return metrics
    except FileNotFoundError:
        print(f"Fichier non trouvé: {yaml_file_path}")
    except PermissionError:
        print(f"Permission refusée: {yaml_file_path}")
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier {yaml_file_path}: {str(e)}")

# Tester la fonction
file_path = 'your_playbook.yml'  # Remplacez par le chemin de votre playbook
metrics = calculate_metrics_playbook("C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml")

if __name__ == '__main__':
    # Convertir les métriques en DataFrame
    if metrics:
        df = pd.DataFrame([metrics])
        print(df)
    else:
        print('Pas de métriques disponibles.')

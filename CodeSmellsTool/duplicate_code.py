import yaml
from collections import Counter

def duplicate_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as e:
        print("Erreur lors de l'analyse du YAML ou du fichier:", e)
        return None

    task_list = []

    if isinstance(data, list):  # Pour les playbooks avec plusieurs plays ou uniquement des tâches
        for play_or_task in data:
            if isinstance(play_or_task, dict):
                # Cas où le playbook contient des plays
                if "tasks" in play_or_task or "block" in play_or_task or "hosts" in play_or_task:
                    #print("hello")
                    if 'tasks' in play_or_task:
                        for task in play_or_task['tasks']:
                            if isinstance(task, dict) and "name" in task:
                                task_params = task.copy()
                                del task_params["name"]
                                task_str = str(sorted(task_params.items()))
                                task_list.append(task_str)
                    if 'block' in play_or_task:
                        for task in play_or_task['block']:
                            if isinstance(task, dict) and "name" in task:
                                task_params = task.copy()
                                del task_params["name"]
                                task_str = str(sorted(task_params.items()))
                                task_list.append(task_str)

                # Cas où le playbook contient uniquement des tâches
                elif "name" in play_or_task:
                    #print("only tasks")
                    task_params = play_or_task.copy()
                    del task_params["name"]
                    task_str = str(sorted(task_params.items()))
                    task_list.append(task_str)

    task_counter = Counter(task_list)
    duplicates = {task: count for task, count in task_counter.items() if count > 1}

    if duplicates:
        return 1
    else:
        return 0

# Tester la fonction
if __name__ == '__main__':
    file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"
    result = duplicate_code(file_path)
    if result is not None:
        print("Code dupliqué détecté" if result == 1 else "Aucun code dupliqué trouvé")
        print(result)

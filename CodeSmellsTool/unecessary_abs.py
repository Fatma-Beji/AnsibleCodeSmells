import yaml

def unecessary_abs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            playbook = yaml.load(f, Loader=yaml.Loader)
    except yaml.YAMLError as e:
        print("Erreur lors de l'analyse du fichier YAML:", e)
        return None
    except FileNotFoundError as e:
        print(f"Fichier {file_path} non trouvé:", e)
        return None

    unnecessary_abstraction_detected = False
    
    for play in playbook:
        tasks = play.get('tasks', [])
        for task in tasks:
            if 'block' in task:
                block_tasks = task['block']
                if len(block_tasks) == 1:
                    unnecessary_abstraction_detected = True
                    break
                    
        if unnecessary_abstraction_detected:
            break

    return 1 if unnecessary_abstraction_detected else 0

# Tester la fonction
if __name__ == "__main__":
    file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"
    result = unecessary_abs(file_path)
    
    if result is not None:
        print(result)

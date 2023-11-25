import os
import pandas as pd
import yaml

def high_coupling(file_path):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return None

    try:
        with open(file_path, 'r') as f:
            playbook = yaml.safe_load(f)
        
        num_imports = 0
        num_roles = 0

        for play in playbook:
            if 'import_playbook' in play:
                num_imports += 1
            
            if 'import_tasks' in play or 'include_tasks' in play:
                num_imports += 1

            if 'roles' in play or 'role' in play:
                roles = play['roles']
                num_roles += len(roles)
                
        metrics = {
            'Num_Imports': num_imports,
            'Num_Roles': num_roles,
        }

        return metrics

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"  
metrics = high_coupling(file_path)

if __name__ == '__main__':
    if metrics:
        df = pd.DataFrame([metrics])
        print(df)
    else:
        print('Pas de métriques disponibles.')

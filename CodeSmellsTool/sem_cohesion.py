import yaml
import nltk
import spacy
import pandas as pd
from nltk.stem import WordNetLemmatizer

# Initialisation du lemmatiseur et du modèle Spacy
lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_lg')

def calculate_similarity(file_path):
    try:
        with open(file_path, 'r', encoding='latin1') as f:
            yaml_data = yaml.load(f, Loader=yaml.Loader)

            if not yaml_data or not isinstance(yaml_data, list):
                print("Le fichier n'est pas un playbook valide")
                return None
        
            sum_similarity = 0
            num_pairs = 0
            
            # plays names
            play_names = [play['name'] for play in yaml_data if 'name' in play]
            #print(play_names)
            preprocessed_play_names = [lemmatizer.lemmatize(name.lower()) for name in play_names]

            for i in range(len(preprocessed_play_names)):
                for j in range(i + 1, len(preprocessed_play_names)):
                    similarity = nlp(preprocessed_play_names[i]).similarity(nlp(preprocessed_play_names[j]))
                    sum_similarity += similarity
                    num_pairs += 1
            # tasks names
            tasks = [task for play in yaml_data if 'tasks' in play for task in play['tasks']]
            task_names = [task['name'] for task in tasks if 'name' in task]
            #print(task_names)
            preprocessed_task_names = [lemmatizer.lemmatize(name.lower()) for name in task_names]

            for i in range(len(preprocessed_task_names)):
                for j in range(i + 1, len(preprocessed_task_names)):
                    similarity_t = nlp(preprocessed_task_names[i]).similarity(nlp(preprocessed_task_names[j]))
                    sum_similarity += similarity_t
                    num_pairs += 1

            if num_pairs > 0:
                average_similarity = sum_similarity / num_pairs
            else:
                average_similarity = 1  # Si aucun pair n'est trouvé, mettre la similarité à 1

            return average_similarity
            
    except Exception as e:
        print(f"Impossible de lire le fichier {file_path}. Erreur: {e}")
        return None

# Tester la fonction
if __name__ == '__main__':
    file_path = 'C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml'  
    average_similarity = calculate_similarity(file_path)
    
    if average_similarity is not None:
        print(f'La similarité moyenne est : {average_similarity}')
    else:
        print('Pas de métriques disponibles.')

import pandas as pd
from collections import defaultdict

# Fonction pour remplir le dictionnaire à partir du DataFrame

def populate_data(df, data):
    current_play = None
    current_playbook = None
    print("---------------")
    for index, row in df.iterrows():
        playbook = row['Playbook Path']
        play = row['Play Name']
        task = row['Task Name']
        #print("---------------")
        if pd.notna(playbook):
            current_playbook = playbook
            data[current_playbook]['smells'] = {}
            for smell in row.index[3:13]:
                data[current_playbook]['smells'][smell] = row[smell]
                #print("playbook",row[smell])

        if pd.notna(play):
            current_play = play
            data[current_playbook][current_play] = {'smells': {}}
            for smell in row.index[14:15]:
                data[current_playbook][current_play]['smells'][smell] = row[smell]
                #print("play",row[smell])

        if pd.notna(task):
            current_task = task
            data[current_playbook][current_play][current_task] = {}
            for smell in row.index[16:17]:
                data[current_playbook][current_play][current_task][smell] = row[smell]
                #print("task",row[smell])

# Charger les fichiers CSV
df1 = pd.read_csv('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Evaluation/test1.csv')
df2 = pd.read_csv('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Evaluation/test2.csv')

# Créer des dictionnaires pour stocker les informations
data1 = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
data2 = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

# Remplir les dictionnaires avec les données des fichiers CSV
populate_data(df1, data1)
print("*********************************************")
populate_data(df2, data2)

# Variables pour calculer la précision et le rappel
true_positive = 0
false_positive = 0
false_negative = 0
true_negative = 0

# Calculer la précision et le rappel en comparant data1 et data2
for playbook in data1.keys():
    #print(data1)
    #print(data2)
    for smell, value in data1[playbook]['smells'].items():
        #print("value ", value)
        true_value = data2[playbook]['smells'].get(smell, None)
        #print("true value ", true_value)
        if true_value is not None:
            if value == true_value:
                if value == 1:
                    true_positive += 1
                else:
                    true_negative += 1
            else:
                if value == 1:
                    false_positive += 1
                else:
                    false_negative += 1

    for play in data1[playbook].keys():
        if play == 'smells':
            continue
        for smell, value in data1[playbook][play]['smells'].items():
            try:
                true_value = data2[playbook][play]['smells'].get(smell, None)
            except KeyError:
                true_value = None
            if true_value is not None:
                if value == true_value:
                    if value == 1:
                        true_positive += 1
                    else:
                        true_negative += 1
                else:
                    if value == 1:
                        false_positive += 1
                    else:
                        false_negative += 1

        for task in data1[playbook][play].keys():
            if task == 'smells':
                continue
            for smell, value in data1[playbook][play][task].items():
                try:
                    true_value = data2[playbook][play][task].get(smell, None)
                except KeyError:
                    true_value = None
                if true_value is not None:
                    if value == true_value:
                        if value == 1:
                            true_positive += 1
                        else:
                            true_negative += 1
                    else:
                        if value == 1:
                            false_positive += 1
                        else:
                            false_negative += 1

# Calculer la précision et le rappel
precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
accuracy = (true_positive + true_negative) / (true_positive + false_positive + false_negative + true_negative) if (true_positive + false_positive + false_negative + true_negative) > 0 else 0


# Afficher les résultats
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"accuracy: {accuracy}")

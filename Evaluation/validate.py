import pandas as pd

# Charger les fichiers CSV
df1 = pd.read_csv('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Evaluation/sorted_manual.csv')
df2 = pd.read_csv('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/Evaluation/sorted_tool_V0.csv')

# Variables pour calculer la précision et le rappel
true_positive = 0
false_positive = 0
false_negative = 0
true_negative = 0

# Fonction pour comparer deux DataFrame
def compare_rows(row1, row2, cols):
    global true_positive, false_positive, false_negative, true_negative
    #print("Comparing rows...")
    for col in cols:
        try:
            val1 = float(row1.iloc[col])
        except TypeError:
            val1 == 0.0
        try:
            val2 = float(row2.iloc[col])
        except TypeError:
            val2 == 0.0

        #print(f"row1.iloc[{col}]: {row1.iloc[col]}, row2.iloc[{col}]: {row2.iloc[col]}")  # Debugging
        if val1 == val2:
            if val1 == 1.0:
                true_positive += 1
            else:
                true_negative += 1
        else:
            if val1 == 1.0:
                false_positive += 1
            else:
                false_negative += 1

for index, row1 in df1.iterrows():
    row2 = df2.iloc[index]

    #print(f"Row {index}")
    if pd.notna(row1['Playbook Path']):
        #print("Comparing Playbook Path...")
        compare_rows(row1, row2,  range(3, 13))

    if pd.notna(row1['Play Name']):
        #print("Comparing Play Name...")
        compare_rows(row1, row2, range(13,15))

    if pd.notna(row1['Task Name']):
        #print("Comparing Task Name...")
        compare_rows(row1, row2, range(15,17))

# Calculer la précision, le rappel et l'exactitude
precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
accuracy = (true_positive + true_negative) / (true_positive + false_positive + false_negative + true_negative) if (true_positive + false_positive + false_negative + true_negative) > 0 else 0

# Afficher les résultats
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"Accuracy: {accuracy}")

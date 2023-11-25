import yaml

def unnamed_play(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as e:
        print("Erreur lors de l'analyse du fichier YAML ou fichier non trouvé :", e)
        return None

    unnamed_plays = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "hosts" in item and "tasks" in item:
                if "name" not in item:
                    unnamed_plays.append(item)

    if unnamed_plays:
        return 1
    else:
        return 0

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"
result = unnamed_play(file_path)
if __name__ == "__main__":
    if result is not None:
        print(result)

import yaml

def detect_overriding_set_fact(yaml_content):
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print("Error parsing YAML:", e)
        return

    set_facts = []
    
    def find_facts_in_data(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "set_fact":
                    if isinstance(value, dict):
                        for fact_name, fact_value in value.items():
                            set_facts.append((fact_name, fact_value))
                else:
                    find_facts_in_data(value)
        elif isinstance(data, list):
            for item in data:
                find_facts_in_data(item)

    def detect_overridden_facts():
        detected_issues = set()
        for fact_name, old_value in set_facts[:-1]:
            for fact_name_next, new_value in set_facts[1:]:
                if fact_name == fact_name_next and old_value != new_value:
                    detected_issues.add(fact_name)
        return detected_issues

    find_facts_in_data(data)
    detected_issues = detect_overridden_facts()
    
    return detected_issues

def overriding_facts(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        smelly_facts = detect_overriding_set_fact(yaml_content)
        
        if smelly_facts:
            return 1
        else:
            return 0

    except Exception as e:
        print(f"Could not read file {file_path}. Error: {e}")
        return None

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"
result = overriding_facts(file_path)
if __name__ == "__main__":
    if result is not None:
        print(result)
    else:
        pass

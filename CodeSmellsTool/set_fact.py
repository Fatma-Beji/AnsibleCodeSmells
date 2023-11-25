import yaml

def find_unnecessary_set_facts(yaml_content):
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print("Error parsing YAML:", e)
        return

    set_facts = set()
    used_facts = set()

    def find_facts_in_data(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "set_fact":
                    if isinstance(value, dict):
                        for fact_name in value.keys():
                            set_facts.add(fact_name)
                else:
                    find_facts_in_data(value)
        elif isinstance(data, list):
            for item in data:
                find_facts_in_data(item)

    find_facts_in_data(data)

    def find_used_facts(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    for fact_name in set_facts:
                        if f"{{{{ {fact_name} }}}}" in value:
                            used_facts.add(fact_name)
                else:
                    find_used_facts(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    for fact_name in set_facts:
                        if f"{{{{ {fact_name} }}}}" in item:
                            used_facts.add(fact_name)
                else:
                    find_used_facts(item)

    find_used_facts(data)
    #print("Set facts:", set_facts)
    #print("Used facts:", used_facts)
    unused_facts = set_facts - used_facts
    return unused_facts

def set_fact(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        unused_facts = find_unnecessary_set_facts(yaml_content)

        if unused_facts:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Could not read file {file_path}. Error: {e}")
        return None

# Tester la fonction
file_path = "C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml"
result = set_fact(file_path)

if __name__ == "__main__":
    if result is not None:
        print(result)
    else:
        pass

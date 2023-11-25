import yaml

def detect_unnecessary_include_vars(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        playbook = yaml.load(f, Loader=yaml.Loader)

    included_vars_files = []
    used_vars = set()

    def find_include_vars(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'include_vars':
                    included_vars_files.append(value)
                elif isinstance(value, (dict, list)):
                    find_include_vars(value)
        elif isinstance(data, list):
            for item in data:
                find_include_vars(item)

    find_include_vars(playbook)

    def find_used_vars(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    for var in included_vars_files:
                        if '{{ ' + var + ' }}' in value:
                            used_vars.add(var)
                elif isinstance(value, (dict, list)):
                    find_used_vars(value)
        elif isinstance(data, list):
            for item in data:
                find_used_vars(item)

    find_used_vars(playbook)

    unused_vars = set(included_vars_files) - set(used_vars)
    return 1 if unused_vars else 0

if __name__ == "__main__":
    result = detect_unnecessary_include_vars('C:/Users/PC/Desktop/mitacs/Projet/ansible/playbooks/parser/expl.yaml')
    print(result)

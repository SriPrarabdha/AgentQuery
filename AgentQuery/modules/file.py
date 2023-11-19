import json
import yaml


def write_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)


def write_json_file(fname, json_str: str):
    json_str = json_str.replace("'", '"')

    data = json.loads(json_str)

    with open(fname, "w") as f:
        json.dump(data, f, indent=4)


def write_yml_file(fname, json_str: str):

    cleaned_json_str = json_str.replace("'", '"')

    try:
        data = json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    with open(fname, "w") as f:
        yaml.dump(data, f)

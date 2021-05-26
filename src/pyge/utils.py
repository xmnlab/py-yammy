import yaml


def read_config(filepath):
    with open(filepath, "r") as f:
        return yaml.load(f)

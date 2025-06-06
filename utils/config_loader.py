import yaml
import os

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up from utils
        config_path = os.path.join(base_dir, "config", "config.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config



# import yaml

# def load_config(config_path: str = r"C:\\agentic-trading-bot\\config\\config.yaml") -> dict:
#     with open(config_path, "r") as file:
#         config = yaml.safe_load(file)
#     return config
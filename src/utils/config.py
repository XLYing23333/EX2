import toml
from .path import Path
import os
from dotenv import load_dotenv

def get_config():
    path = Path()
    if not hasattr(path, 'config'):
        raise AttributeError("Path object has no attribute 'config'")
    if not os.path.exists(path.config):
        raise FileNotFoundError(f"Config file not found: {path.config}")
    try:
        with open(path.config, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        if not isinstance(config, dict):
            raise ValueError("Config file contents is not a valid TOML dictionary")
    except Exception as e:
        raise RuntimeError(f"Failed to load config: {e}")
    return config

def get_config_value(types, key):
    if not isinstance(types, str) or not isinstance(key, str):
        raise TypeError("`types` and `key` must be strings")
    config = get_config()
    if types not in config:
        raise KeyError(f"Section '{types}' not in config")
    if key not in config[types]:
        raise KeyError(f"Key '{key}' not in config section '{types}'")
    return config[types][key]
    
def change_config(types, key, value):
    if not isinstance(types, str) or not isinstance(key, str):
        raise TypeError("`types` and `key` must be strings")
    path = Path()
    config = get_config()
    if types not in config or not isinstance(config[types], dict):
        raise KeyError(f"Section '{types}' not in config or not a mapping")
    config[types][key] = value
    try:
        with open(path.config, 'w', encoding='utf-8') as f:
            toml.dump(config, f)
    except Exception as e:
        raise RuntimeError(f"Failed to write config: {e}")

def get_models(group):
    '''
    models, configs = get_models(group)
    '''
    if not isinstance(group, str):
        raise TypeError("`group` must be a string")
    config = get_config()
    if 'MODEL' not in config or group not in config['MODEL']:
        raise KeyError(f"Group '{group}' not found in MODEL section")
    group_config = config['MODEL'][group]
    if not isinstance(group_config, dict):
        raise ValueError(f"MODEL[group] is not a dictionary")
    models = list(group_config.keys())
    return models, group_config

def get_key(group):
    load_dotenv()
    if not isinstance(group, str):
        raise TypeError("`group` must be a string")
    key = os.getenv(f'KEY_{group}')
    return key

def get_model_info(model_id):
    """
    Get model info from config.toml
    """
    if not isinstance(model_id, str):
        raise TypeError("`model_id` must be a string")
    config = get_config()
    model_group = None
    msg = None
    if "MODEL" not in config:
        raise KeyError("MODEL section not in config")
    for group in config['MODEL']:
        if model_id in config['MODEL'][group]:
            msg = dict(config['MODEL'][group][model_id])
            model_group = group
            break
    if not msg or not model_group:
        raise KeyError(f"Model ID '{model_id}' not found in config")
    if model_group == "OLLAMA":
        msg['key'] = None
    else:
        msg['key'] = get_key(model_group)
    msg['group'] = model_group
    return msg

def get_full_models():
    print("[DATA] ALL MODELS:")
    config = get_config()
    if 'MODEL' not in config or not isinstance(config['MODEL'], dict):
        raise KeyError("MODEL section missing or invalid in config")
    models = []
    for group in config['MODEL']:
        try:
            models_temp, _ = get_models(group)
            models += models_temp
        except Exception:
            continue
    return models


if __name__ == '__main__':
    try:
        get_config()
    except Exception as e:
        print(f"Error: {e}")
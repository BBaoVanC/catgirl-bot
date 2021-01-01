# settings.py
# handles getting, saving, setting config
# also handles directory creation
import os, cfg

def make_dir_if_needed(path):
    if not os.path.exists(path):
        os.mkdir(path)

def default_config() -> dict:
    return {
        'filterRole' : '1', # so none, but store an int
        'filter' : [],
        'prefix' : '?',
        'loggingEnabled' : 'yes',
        'modrole' : '1' # same here
    }

def get_value(section, key) -> object:
    return cfg.config[str(section)][str(key)]

# just to make it look nicer in other files
def get_integer_value(section, key) -> int:
    return int(get_value(section, key))

def get_boolean_value(section, key) -> bool:
    return cfg.config.getboolean(str(section), str(key))

def save_config():
    file = open(f'config/bot/settings.ini', 'w')
    cfg.config.write(file)
    file.close()

def set_value(section, key, value):
    cfg.config[str(section)][str(key)] = value
    save_config()
    
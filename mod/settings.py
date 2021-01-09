#!/usr/bin/env python3
# settings.py
# handles getting, saving, setting config
# also handles directory creation
import os, cfg

def default_config() -> dict:
    return {
        'filterRole' : '1', # so none, but store an int
        'filter' : [],
        'prefix' : '?',
        'loggingEnabled' : 'yes',
        'modrole' : '1', # same here
        'logchannel' : '1',
        'reactions' : 'yes'
    }

def get_value(section, key) -> object:
    try:
        return cfg.config[str(section)][str(key)]
    except:
        # return nothing
        return None

# just to make it look nicer in other files
def get_integer_value(section, key) -> int:
    try:
        return int(get_value(section, key))
    except:
        # default to 1
        return 1

def get_boolean_value(section, key, default) -> bool:
    try:
        return cfg.config.getboolean(str(section), str(key))
    except:
        return default

def save_config():
    file = open(f'config/bot/settings.ini', 'w')
    cfg.config.write(file)
    file.close()

def set_value(section, key, value):
    cfg.config[str(section)][str(key)] = value
    save_config()
    
#!/usr/bin/env python3
# filemanager.py
# handles files n shit
# iirc shutil is python 3 only
import os, shutil, cfg, settings

def make_dir_if_needed(path):
    # this does not need a comment
    if not os.path.exists(path):
        os.mkdir(path)

async def make_zip_file(guild) -> str:

    temp_folder = f'tmp/{guild.id}'
    make_dir_if_needed(temp_folder)

    # archive guild logs to a zip file with shutil
    shutil.make_archive(f'{temp_folder}/{guild.name}', 'zip', f'logs/guilds/{guild.id}')
    return f'{temp_folder}/{guild.name}.zip'

def make_initial_dirs():

    # define the dirs we need
    needed_dirs = [
        'tmp',
        'logs',
        'logs/botevent',
        'logs/guilds',
        'config',
        'config/bot'
    ]

    # enumerate through and create if they don't exist
    for dir in needed_dirs:
        make_dir_if_needed(dir)


def setup_guilds_config(guilds):
    # setup for each guild
    for guild in guilds:
        # :fr:
        if guild.name == None:
            return

        # if config for guild not existing, create
        if not str(guild.id) in cfg.config.sections():
            cfg.config[guild.id] = settings.default_config()

            # write changes
            settings.save_config()
        
        # make logs for each guild
        make_dir_if_needed(f'logs/guilds/{guild.id}')

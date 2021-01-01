# file manager.py
# handles files n shit
# iirc shutil is python 3 only
import os
import shutil

def make_dir_if_needed(path):
    if not os.path.exists(path):
        os.mkdir(path)

async def make_zip_file(guild) -> str:

    temp_folder = f'tmp/{guild.id}'
    make_dir_if_needed(temp_folder)

    shutil.make_archive(f'{temp_folder}/{guild.name}', 'zip', f'logs/guilds/{guild.id}')
    return f'{temp_folder}/{guild.name}.zip'

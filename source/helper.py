#!/usr/bin/env python3
""" Helper function to copy html files to docs folder """
import os
import shutil
from pathlib import Path

# pylint: disable=trailing-whitespace

def helper():
    """ Helper function to copy html files to docs folder """
    og_dest = '../../docs/html'
    dest = '../../docs'
    if os.path.exists('../../docs/html'):
        os.system(f'chmod +rw {og_dest}/*.*')
        for file in Path(og_dest).glob('*.*'):
            shutil.copy(os.path.join(og_dest, file), dest)
            folder_names = ['_static', '_sources']
        for folder in folder_names:
            folder_dest = os.path.join(og_dest, folder)
            os.system(f'chmod +rw {folder_dest}')
            shutil.copytree(folder_dest, dest + f'/{folder}', dirs_exist_ok=True)

if __name__ == '__main__':
    helper()

# -*- coding: utf-8 -*-
import shutil
import os
import config

def save_token(token):
    with open(config.path_token, 'w') as f:
        f.write(token)
        
def delete_folder_anyway(dirpath):
    try:
        shutil.rmtree(dirpath)
    except:
        pass
        
def delete_file_anyway(filepath):
    try:
        os.remove(filepath)
    except:
        pass
        
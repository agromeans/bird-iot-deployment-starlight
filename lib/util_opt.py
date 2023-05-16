# -*- coding: utf-8 -*-
from lib.logger_opt import *
import shutil
import os
import config
from configparser import ConfigParser

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
        
def read_config_value(filepath, section, key):
    _config = ConfigParser()
    try:
        _config.read(filepath)
        return _config.get(section, key)
    except Exception as e:
        logger.warning(str(e))
        return ''
        
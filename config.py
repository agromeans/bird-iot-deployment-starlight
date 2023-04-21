# -*- coding: utf-8 -*-
from configparser import ConfigParser
from lib.logger_opt import *

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

version = ''

path_root = ''
path_token = ''
path_frpc = ''
path_github = ''
frp_server = ''
frp_user = ''

api_token_get = ''
token = ''

def get_version():
    return version
    
def check_config_section():
    if not config.has_section('common'):
        config.add_section('common')
        
    if not config.has_section('path'):
        config.add_section('path')
        
    if not config.has_section('api'):
        config.add_section('api')
        
    config.write(open(config_file, 'w'))
    
def get_config():
    global version, path_root, path_token, path_frpc, path_github, api_token_get
    
    try:
        version = config.get('common', 'version')
    except Exception as e:
        logger.warning(e)
        print(e)
        version = ''
        
    try:
        path_root = config.get('path', 'root')
    except Exception as e:
        logger.warning(e)
        print(e)
        path_root = ''
        
    try:
        path_token = config.get('path', 'token')
    except Exception as e:
        logger.warning(e)
        print(e)
        path_token = ''
        
    try:
        path_frpc = config.get('path', 'frpc')
    except Exception as e:
        logger.warning(e)
        print(e)
        path_frpc = ''
        
    try:
        path_github = config.get('path', 'github')
    except Exception as e:
        logger.warning(e)
        print(e)
        path_github = ''
        
    try:
        api_token_get = config.get('api', 'token_get')
    except Exception as e:
        logger.warning(e)
        print(e)
        api_token_get = ''
        
def get_frpc():
    global frp_server, frp_user
    
    _config = ConfigParser()
    _config.read(path_frpc)
    
    try:
        frp_server = _config.get('common', 'server_addr')
    except Exception as e:
        logger.warning(e)
        print(e)
        frp_server = ''
        
    try:
        frp_user = _config.get('ssh', 'remote_port')
    except Exception as e:
        logger.warning(e)
        print(e)
        frp_user = ''
        
    # logger.info(f"====The device is using ssh frp: {frp_server}:{frp_user}====")
    
def get_token():
    global token
    
    try:
        with open(path_token, 'r') as f:
            token = f.readline().rstrip()
    except:
        token = ''
        
def reload_config():
    check_config_section()
    get_config()
    get_frpc()
    get_token()
    
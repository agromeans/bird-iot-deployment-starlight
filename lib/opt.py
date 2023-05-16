# -*- coding: utf-8 -*-
from lib.logger_opt import *
import json
import config
import requests

requests.packages.urllib3.disable_warnings()

def get_hub_info_from_server(server, service_name):
    d = {
        'frp': f"{config.frp_server}:{config.frp_user}",
        'service_name': service_name
    }
    
    try:
        r = requests.post(f"https://{server}{config.api_hub_info_get}", json=d, verify=False, timeout=(3, 10))
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return None
        
    try:
        if r.json().get('status_code') != 200:
            logger.error('Server service is abnormal.')
            return None
            
        return r.json().get('message').get('repo_hub')
    except json.decoder.JSONDecodeError:
        logger.error('The server service response format is invalid.')
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return None
        
def get_version_from_server(server):
    d = {
        'frp': f"{config.frp_server}:{config.frp_user}"
    }
    
    try:
        r = requests.post(f"https://{server}{config.api_version_get}", json=d, verify=False, timeout=(3, 10))
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return []
        
    try:
        if r.json().get('status_code') != 200:
            logger.error('Server service is abnormal.')
            return []
            
        if not isinstance(r.json().get('message'), list):
            logger.error('The server service response format is invalid.')
            return []
            
        return r.json().get('message')
    except json.decoder.JSONDecodeError:
        logger.error('The server service response format is invalid.')
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return []
        
def get_info_from_server(server):
    d = {
        'frp': f"{config.frp_server}:{config.frp_user}"
    }
    
    try:
        r = requests.post(f"https://{server}{config.api_token_get}", json=d, verify=False, timeout=(3, 10))
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return None, None
        
    try:
        if r.json().get('status_code') != 200:
            logger.error('Server service is abnormal.')
            return None, None
        return r.json().get('message').get('token'), r.json().get('message').get('github')
    except json.decoder.JSONDecodeError:
        logger.error('The server service response format is invalid.')
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return None, None
        
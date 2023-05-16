# -*- coding: utf-8 -*-
from lib.logger_opt import *
import lib.opt as opt
import lib.util_opt as util
import config
import os
import argparse

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', '--server', type=str, required=True, help='api server ip port')
    return parser.parse_args()
    
def run(args):
    # 1. get version list from server api
    verison_list = opt.get_version_from_server(args.server)
    
    # 2. get the version from itself services
    for item in verison_list:
        service_name = item.get('service_name')
        new_version = item.get('version')
        
        os.system(f"docker exec {service_name} cat agromeans/config.ini > {service_name}.txt")
        itself_version = util.read_config_value(f"{service_name}.txt", 'common', 'version')
        
        # 3. check the version is equal
        if itself_version != new_version:
            # 4. get hub url if the version is not equal
            hub_info = opt.get_hub_info_from_server(args.server, service_name)
            hub_name = hub_info.split('agromeans/')[1].replace('.git', '')
            repo_name = hub_name.replace('-hub', '')
            
            # 5. remove hub and itself_version.txt
            util.delete_folder_anyway(hub_name)
            util.delete_file_anyway(f"{service_name}.txt")
            
            # 6. git clone hub, cd in the hub
            os.system(f"git clone --depth 1 {hub_info}")
            
            # 7. tar -zxvf package
            os.system(f"cd {hub_name} && tar -zxvf package.tar.gz")
            
            # 8. remove docker image and container
            os.system(f"docker rm -f {service_name}")
            os.system(f"docker rmi {service_name}")
            
            # 9. docker build and docker-compose up
            os.system(f"docker build -t {service_name} {hub_name}/{repo_name}/ --no-cache")
            os.system(f"/usr/local/bin/docker-compose -f {hub_name}/{repo_name}/docker-compose.yml up -d")
            
            # 10. remove hub and itself_version.txt
            util.delete_folder_anyway(hub_name)
            
if __name__ == "__main__":
    args = process_command()
    config.reload_config()
    run(args)
    
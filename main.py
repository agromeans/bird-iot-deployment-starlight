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
    # 1. check and save token
    token, _ = opt.get_info_from_server(args.server)
    if token is None:
        logger.error('device token is null, end process')
    util.save_token(token)
    
    # 2. get version list from server api
    verison_list = opt.get_version_from_server(args.server)
    
    # 3. get the version from itself services
    for item in verison_list:
        service_name = item.get('service_name')
        new_version = item.get('version')
        
        os.system(f"docker exec {service_name} cat agromeans/config.ini > {service_name}.txt")
        itself_version = util.read_config_value(f"{service_name}.txt", 'common', 'version').strip()
        
        # 4. check the version is equal
        if itself_version != new_version:
            # 5. get hub url if the version is not equal
            hub_info, mkdir_list = opt.get_hub_info_from_server(args.server, service_name)
            hub_name = hub_info.split('/')[-1].replace('.git', '')
            repo_name = hub_name.replace('-hub', '')
            
            # 6. remove hub and itself_version.txt
            util.delete_folder_anyway(hub_name)
            
            # 7. madir for folders
            for _dir in mkdir_list:
                os.system(f"mkdir -p {_dir}")
                
            # 8. git clone hub, cd in the hub
            os.system(f"git clone --depth 1 {hub_info}")
            
            # 9. tar -zxvf package
            os.system(f"cd {hub_name} && tar -zxvf package.tar.gz")
            
            # 10. remove docker image and container
            os.system(f"docker rm -f {service_name}")
            os.system(f"docker rmi {service_name}")
            
            # 11. docker build and docker-compose up
            os.system(f"docker build -t {service_name} {hub_name}/{repo_name}/ --no-cache")
            os.system(f"/usr/local/bin/docker-compose -f {hub_name}/{repo_name}/docker-compose.yml up -d")
            
            # 12. remove hub and itself_version.txt
            util.delete_folder_anyway(hub_name)
            
        util.delete_file_anyway(f"{service_name}.txt")
if __name__ == "__main__":
    args = process_command()
    config.reload_config()
    run(args)
    
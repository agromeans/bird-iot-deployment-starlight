# -*- coding: utf-8 -*-
from lib.logger_opt import *
import lib.opt as opt
import lib.util_opt as util
import config
import subprocess
import os
import shutil
import argparse

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', '--server', type=str, required=True, help='api server ip port')
    parser.add_argument('-repo', '--repo', type=str, required=True, help='git repod')
    return parser.parse_args()
    
def run(args):
    # 1. 使用shell啟動python程式，在crontab內設定觸發shell頻率(1hr)，透過參數來區分要升級的服務
    util.delete_folder_anyway(os.path.join(config.path_root, args.repo))
    util.delete_file_anyway(os.path.join(config.path_root, f"{args.repo}.sh"))
    
    # 2. 取出frp資訊向伺服器取得token與github ip(更新github.txt)，若有token則繼續下一步，否則停止此次流程
    # 2.1. get token and github
    token, github = opt.get_info_from_server(args.server)
    if not token or not github:
        return
        
    # 2.2. save token
    util.save_token(token)
    
    # 3. git clone對應repo到根目錄下，從repo中取出部署用shell
    # 3.1. git clone to root/{repo}, check dir and shell
    subprocess.run(['git', 'clone', f"git@{github}:agromeans/{args.repo}.git", f"{os.path.join(config.path_root, args.repo)}"], check=True)
    
    # 3.2. check dir and shell
    if not os.path.isdir(os.path.join(config.path_root, args.repo)):
        logger.error('folder not exist', exc_info=True)
        return
        
    if not os.path.exists(os.path.join(config.path_root, args.repo, 'docker-deployment.sh')):
        logger.error('deployment shell not exist', exc_info=True)
        return
        
    # 3.3. move deployment shell(搬移時改名為$repo)
    shutil.move(os.path.join(config.path_root, args.repo, 'docker-deployment.sh'), os.path.join(config.path_root, f"{args.repo}.sh"))
    
if __name__ == "__main__":
    args = process_command()
    config.reload_config()
    run(args)
    
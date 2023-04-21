# -*- coding: utf-8 -*-
from lib.logger_opt import *
import lib.opt as opt
import lib.util_opt as util
import config
import time
import argparse

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', '--server', type=str, required=True, help='api server ip port')
    return parser.parse_args()
    
def run(args):
    while True:
        try:
            # 取出frp資訊向伺服器取得token，若有token則更新檔案
            # 1. get token
            token, _ = opt.get_info_from_server(args.server)
            if not token:
                raise Exception('This device is not registered.')
                
            # 2. save token
            if token == config.token:
                logger.info(f"The token '{token}' has not changed, stop get_token program.")
                return
                
            logger.info(f"The token becomes a new value '{token}' and stores it.")
            util.save_token(token)
        except Exception as e:
            logger.error(f"{str(e)}")
        finally:
            time.sleep(5)
            
if __name__ == "__main__":
    time.sleep(60)
    args = process_command()
    config.reload_config()
    run(args)
    

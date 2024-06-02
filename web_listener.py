import json
from github import Github
import falcon
import logging

#Global
logger=None
config_json={}
settings_file="./settings.json"

def ensure_logger():
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='github-updater.log', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
def main():
    ensure_logger()
    with open(settings_file, "r") as _f:
        try:
            global config_json
            config_json = json.load(_f)
        except IOError:
            logger.warning(f"Couldn't load {settings_file}")
            print(f"Couldn't load {settings_file}")
        finally:
            if config_json != {}:
                print(config_json['repos'][0]['endpoints'][0]['local_dir'])
                          
if __name__ == "__main__":
    main()            
import json
from github import Github
import falcon
import logging

#Global
logger=None
config_json=None
settings_file="./settings.json"

def ensure_logger():
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='chatgpt-discord-bot.log', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
def main():
    ensure_logger()
    with open(settings_file, "r") as _f:
        try:
            config_json = json.load(_f.read())
        except IOError:
            logger.warning(f"Couldn't load {settings_file}")
        finally:
            if config_json is not None:
                #TODO
                return
if __name__ == "__main__":
    main()            
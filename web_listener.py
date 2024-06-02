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
class EndpointClass:
    def __init__(self, endpoint, repo_name, local_dir, remote_user, remote_name, remote_branch):
        self.endpoint = endpoint
        self.repo_name = repo_name
        self.local_dir = local_dir
        self.remote_user = remote_user
        self.remote_name = remote_name
        self.remote_branch = remote_branch

class ListenerClass:
    #TODO EXTENDS SOMETHING??
    
def create_listeners(endpoints_list):
     for endpoint in endpoints_list:
              #TODO SEE FALCON DOCS
        
def main():
    
    def warn_settings():
        logger.warning(f"Could not find usable settings. Check {settings_file} for proper json syntax. See github for structure.")            
    
    #START
    ensure_logger()
    with open(settings_file, "r") as _f:
        try:
            global config_json
            config_json = json.load(_f)
        except IOError:
            warn_settings()
            print(f"Couldn't load {settings_file}")
        finally:
            if config_json != {}:
                endpoints=[]
                for endpoint in config_json['endpoints']:
                    logger.info(f"Starting endpoint: {endpoint["endpoint"]}")
                    logger.debug(f"Starting endpoint: {endpoint}")
                    new_endpoint = EndpointClass(endpoint["endpoint"], endpoint["repo_name"], endpoint["local_dir"], endpoint["remote_user"], endpoint["remote_name"], endpoint["remote_branch"])
                    endpoints.append(new_endpoint)
            if endpoints != []:
                create_listeners(endpoints)
            else:
                warn_settings()

if __name__ == "__main__":
    main()            
import json
from wsgiref.simple_server import make_server
import falcon
import logging
import subprocess
import re 

#Global
logger=None
config_json={}
settings_file="./settings.json"
active_endpoints=[]
endpoint_handler=None
app = None

def ensure_logger():
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='github-updater.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def restart_service(service_name):
    result = subprocess.run(str(f"sudo systemctl restart {service_name}.service"), capture_output = True, text = True, shell=True)
    logger.debug(f"Restart {service_name} - Result: {result.stdout}")
    logger.debug(f"Restart {service_name} - Error: {result.stderr}")

def git_command(endpoint):
    github_url=str(f"https://github.com/{endpoint.remote_user}/{endpoint.repo_name} {endpoint.remote_name} {endpoint.remote_branch}")                      
    working_dir=str(f"{endpoint.local_dir}/{endpoint.repo_name}")
    result = subprocess.run(str(f"cd {working_dir} && git fetch && git pull {github_url}"), capture_output = True, text = True, shell=True)
    logger.debug(f"Git {endpoint} - Result: {result.stdout}")
    logger.debug(f"Git {endpoint} - Error: {result.stderr}")

    restart_service(endpoint.service_name)

class EndpointHandler:
    def get_branch(self, ref):
        ensure_logger()
        logger.debug(f"Ref: {ref}")
        branch = re.search("(?<=/refs/heads/).*", ref)
        return branch

    def on_post(self, req, resp):
        ensure_logger()
        resp.status = falcon.HTTP_200
        branch = self.get_branch(json.dumps(req.media["ref"]))
        logger.debug(f"Branch: {branch}")
        for endpoint in active_endpoints:
            if req.path == endpoint.endpoint:
                if branch == endpoint.remote_branch:
                    git_command(endpoint)

class EndpointClass:
    def __init__(self, endpoint, repo_name, local_dir, remote_user, remote_name, remote_branch, service_name):
        self.endpoint = endpoint
        self.repo_name = repo_name
        self.local_dir = local_dir
        self.remote_user = remote_user
        self.remote_name = remote_name
        self.remote_branch = remote_branch
        self.service_name = service_name

def create_listeners(endpoints_list):
    for endpoint in endpoints_list:
        try:
            app.add_route(endpoint.endpoint, endpoint_handler)
            global active_endpoints
            active_endpoints.append(endpoint)
        except Exception as e:
            print(f"Could not add endpoint: {endpoint}. {e}")
def main():
    
    def warn_settings():
        logger.warning(f"Could not find usable settings. Check {settings_file} for proper json syntax. See github for structure.")            
    
    #START
    ensure_logger()

    global endpoint_handler
    endpoint_handler = EndpointHandler()

    global app
    app = falcon.App()
    
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
                    logger.debug(f"Starting endpoint: {endpoint}")
                    new_endpoint = EndpointClass(endpoint["endpoint"], endpoint["repo_name"], endpoint["local_dir"], endpoint["remote_user"], endpoint["remote_name"], endpoint["remote_branch"], endpoint["service_name"])
                    endpoints.append(new_endpoint)
            if endpoints != []:
                create_listeners(endpoints)
            else:
                warn_settings()

    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()            

if __name__ == "__main__":
    main()            
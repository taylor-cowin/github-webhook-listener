This python app listens on port 8000 (unless otherwise specified) for POST requests to a specified URL. It's intended to be used with github webhooks but could be adapted to other uses easily. Once a request is received, it pulls the repo associated with the endpoint POSTed to and then restarts the service hosting the repo's code (or whatever service is specified).

Partial roadmap:

>Better logging!!!
>Adding port, interface, and other options to the settings file
>Example settings values (and maybe stop using json for handling the settings?)
>Make service handling optional instead of mandatory
>Handling of private repos (might currently work with ssh-add but is untested)

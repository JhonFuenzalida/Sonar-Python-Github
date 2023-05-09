This script permits to :

- add github SSO authentification inside sonar
- create of all your github teams inside sonar (as sonar groups)
- create a project on sonar for all your github repos (required for next step because repos needs to be created to synchronize the rights)
- synchronize the rights on sonar projects with those on github repos

To make this script work, you need to :

- create a github personnal token
- create a sonar token
- configure .env with variables

run the following commands:

`virtualenv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python sonar-github.py`

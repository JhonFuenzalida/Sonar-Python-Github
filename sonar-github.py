from github import Github
from decouple import config
from sonarqube import SonarQubeClient
g = Github(config('GITHUB_PERSONAL_KEY'))
s = SonarQubeClient(sonarqube_url=config('SONARQUBE_URL'), token=config('SONARQUBE_TOKEN'))

org_name = "Keiron-HealthTech"
if(s.alm_settings.get('github')) == None:
    clientid=config('GITHUB_CLIENTID') 
    clientsecret = config('GITHUB_CLIENTSECRET')
    s.settings.update_setting_value(key='sonar.auth.github.enabled', value="true") #permits to enable the authentification with github
    s.settings.update_setting_value(key='sonar.auth.github.clientId.secured', value=clientid) 
    s.settings.update_setting_value(key='sonar.auth.github.clientSecret.secured', value=clientsecret) 
    s.settings.update_setting_value(key='sonar.auth.github.allowUsersToSignUp', value="true")
    s.settings.update_setting_value(key='sonar.auth.github.groupsSync', value="true") #synchronize the groups between sonar and github
    s.settings.update_setting_value(key='sonar.auth.github.organizations', values=org_name)
    with open(config('PEM_FILE')) as file:
        privatekey = file.read()
    s.alm_settings.create_github(appId = "202099", clientId=clientid, clientSecret=clientsecret, key="github", privateKey=privatekey, url="https://api.github.com/")
org = g.get_organization(org_name)
for team in org.get_teams():
    group_name = org_name +"/" +team.name.replace(" ", "-")
    group_exist = False
    groups = s.user_groups.search_user_groups()
    for group in groups['groups']:
        if group_name == group['name'].replace(" ", "-"):
            group_exist = True
    if group_exist == False:
        s.user_groups.create_group(name=group_name, description=team.name)
    
    for repo in team.get_repos():
        project_exist = False
        projectstr = repo.full_name.split('/')
        projectName = projectstr[1]
        projects = s.projects.search_projects()
        teamName = team.name.replace(" ", "-")
        for project in projects["components"]:
            if projectName == project['name']:
                project_exist = True
        if project_exist == False:
            s.projects.create_project(project=projectName, name=projectName, visibility="private")
        s.permissions.add_permission_to_group(groupName= org_name + "/"+ teamName, permission="scan", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + teamName, permission="codeviewer", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + teamName, permission="user", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + teamName, permission="issueadmin", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + teamName, permission="securityhotspotadmin", projectKey=projectName)

# admin_group_name = "" #add the name of the github team who would be admin of your sonar instance
# s.permissions.add_permission_to_group(groupName= org_name + "/" + admin_group_name, permission="admin")

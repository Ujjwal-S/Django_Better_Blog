# contains the code which updates the code on pythonanywhere.

import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("better-blog") 
        origin = repo.remotes.origin

        origin.pull()

        import requests
    
        with open(os.path.join(settings.BASE_DIR, 'secrets.json')) as secret_file:
            secret = json.load(secret_file)

        username = "betterblog"
        api_token = secret["PYTHONANYWHERE_API_TOKEN"]
        domain_name = "betterblog.pythonanywhere.com"

        response = requests.post(
            'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
                username=username, domain_name=domain_name
            ),
            headers={'Authorization': 'Token {token}'.format(token=api_token)}
        )
        
        if response.status_code == 200:
            return HttpResponse("Updated code on PythonAnywhere")
        else:
            return HttpResponse("some error occured.")

    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere...")

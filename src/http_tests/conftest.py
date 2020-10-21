'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain, Jordan Hunyh, Ahmet Karatas,
              Cyrus Wilkie, Joseph Knox

Iteration 2
'''

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest

# need to plan how to format this
'''
****************************BASIC TEMPLATE******************************
'''

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture
def reset(url):
    '''
    Resets the internal data of the application to it's initial state
    '''

    requests.post(f"{url}/clear")

@pytest.fixture
def initialise_user_data(reset):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    admin_details = requests.post(f"{url}/auth/register", json={
        'email': 'admin@email.com',
        'password': 'admin_pass1!',
        'name_first': 'admin_first',
        'name_last': 'admin_last'
    }).json()

    user1_details = requests.post(f"{url}/auth/register", json={
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }).json()

    user2_details = requests.post(f"{url}/auth/register", json={
        'email': 'user2@email.com',
        'password': 'user2_pass1!',
        'name_first': 'user2_first',
        'name_last': 'user2_last'
    }).json()

    return {
        'admin': admin_details,
        'user1': user1_details,
        'user2': user2_details
    }

@pytest.fixture
def initialise_channel_data(initialise_user_data):
    '''
    creates 3 channels with descriptive data for testing
    '''

    public_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['admin']['token'],
        'name': 'public',
        'is_public': True
    }).json()

    private_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['admin']['token'],
        'name': 'private1',
        'is_public': False
    }).json()

    user_private_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['user1']['token'],
        'name': 'private2',
        'is_public': False
    }).json()

    return {
        'admin_publ': public_details,
        'admin_priv': private_details,
        'user1_priv': user_private_details
    }

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
def initialise_user_data(url):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    user0_details = requests.post(f"{url}/auth/register", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }).json()

    user1_details = requests.post(f"{url}/auth/register", json={
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }).json()

    user3_details = requests.post(f"{url}/auth/register", json={
        'email': 'user3@email.com',
        'password': 'user3_pass1!',
        'name_first': 'user3_first',
        'name_last': 'user3_last'
    }).json()

    user4_details = requests.post(f"{url}/auth/register", json={
        'email': 'user4@email.com',
        'password': 'user4_pass1!',
        'name_first': 'user4_first',
        'name_last': 'user4_last'
    }).json()

    user5_details = requests.post(f"{url}/auth/register", json={
        'email': 'user5@email.com',
        'password': 'user5_pass1!',
        'name_first': 'user5_first',
        'name_last': 'user5_last'
    }).json()

    user6_details = requests.post(f"{url}/auth/register", json={
        'email': 'user6@email.com',
        'password': 'user6_pass1!',
        'name_first': 'user6_first',
        'name_last': 'user6_last'
    }).json()

    user7_details = requests.post(f"{url}/auth/register", json={
        'email': 'user7@email.com',
        'password': 'user7_pass1!',
        'name_first': 'user7_first',
        'name_last': 'user7_last'
    }).json()

    user8_details = requests.post(f"{url}/auth/register", json={
        'email': 'user8@email.com',
        'password': 'user8_pass1!',
        'name_first': 'user8_first',
        'name_last': 'user8_last'
    }).json()

    user9_details = requests.post(f"{url}/auth/register", json={
        'email': 'user9@email.com',
        'password': 'user9_pass1!',
        'name_first': 'user9_first',
        'name_last': 'user9_last'
    }).json()

    user10_details = requests.post(f"{url}/auth/register", json={
        'email': 'user10@email.com',
        'password': 'user10_pass1!',
        'name_first': 'user10_first',
        'name_last': 'user10_last'
    }).json()

    user11_details = requests.post(f"{url}/auth/register", json={
        'email': 'user11@email.com',
        'password': 'user11_pass1!',
        'name_first': 'user11_first',
        'name_last': 'user11_last'
    }).json()

    return {
        'user0': user0_details,
        'user1': user1_details
        'user2': user0_details,
        'user3': user0_details,
        'user4': user0_details,
        'user5': user0_details,
        'user6': user0_details,
        'user7': user0_details,
        'user8': user0_details,
        'user9': user0_details,
        'user10': user0_details,
        'user12': user0_details,
    }

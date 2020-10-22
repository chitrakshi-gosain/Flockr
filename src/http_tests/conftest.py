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

    requests.delete(f"{url}/clear")

@pytest.fixture
def initialise_user_dictionary(reset):

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }

    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_FIRST',
        'name_last': 'user1_LAST'
    }
    
    user2 = {
        'email': 'user2@email.com',
        'password': 'user2_pass1!',
        'name_first': 'user2_FIRST',
        'name_last': 'user2_LAST'
    }

    user3 = {
        'email': 'user3@email.com',
        'password': 'user3_pass1!',
        'name_first': 'user3_FIRST',
        'name_last': 'user3_LAST'
    }
    
    return {
        'user0_dict': user0,
        'user1_dict': user1,
        'user2_dict': user2,
        'user3_dict': user3
    }

@pytest.fixture
def initialise_user_data(url, initialise_user_dictionary):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''
    user0 = initialise_user_dictionary['user0_dict']
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()

    user1 = initialise_user_dictionary['user1_dict']
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()

    user2 = initialise_user_dictionary['user2_dict']
    user2_details = requests.post(f"{url}/auth/register", json=user2).json()

    user3 = initialise_user_dictionary['user3_dict']
    user3_details = requests.post(f"{url}/auth/register", json=user3).json()

    return {
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details
    }

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Chitrakshi Gosain, Jordan Hunyh, Ahmet Karatas,
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

'''
****************************BASIC TEMPLATE******************************
'''

'''
This file contains all the fixtures used in *http_test.py
'''

'''
APP.routes_USED_FOR_THIS_FIXTURE_FILE("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
   json.dumps({channel_id})
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
    '''
    Creates dictionaries with descriptive user data for testing
    purposes and returns user data which is implementation dependent
    '''

    admin = {
        'email': 'admin@email.com',
        'password': 'admin_pass1!',
        'name_first': 'admin_first',
        'name_last': 'admin_last'
    }

    owner = {
        'email': 'owner@email.com',
        'password': 'owner_pass1!',
        'name_first': 'owner_first',
        'name_last': 'owner_last'
    }

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user2 = {
        'email': 'user2@email.com',
        'password': 'user2_pass1!',
        'name_first': 'user2_first',
        'name_last': 'user2_last'
    }

    user3 = {
        'email': 'user3@email.com',
        'password': 'user3_pass1!',
        'name_first': 'user3_first',
        'name_last': 'user3_last'
    }

    return {
        'admin_dict': admin,
        'owner_dict': owner,
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

    admin = initialise_user_dictionary['admin_dict']
    admin_details = requests.post(f"{url}/auth/register", json=admin).json()

    owner= initialise_user_dictionary['owner_dict']
    owner_details = requests.post(f"{url}/auth/register", json=owner).json()

    user0 = initialise_user_dictionary['user0_dict']
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()

    user1 = initialise_user_dictionary['user1_dict']
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()

    user2 = initialise_user_dictionary['user2_dict']
    user2_details = requests.post(f"{url}/auth/register", json=user2).json()

    user3 = initialise_user_dictionary['user3_dict']
    user3_details = requests.post(f"{url}/auth/register", json=user3).json()

    return {
        'admin': admin_details,
        'owner': owner_details,
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details
    }


@pytest.fixture
def initialise_channel_data(url, initialise_user_data):
    '''
    Creates few channels with descriptive data for testing
    '''

    admin_public_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['admin']['token'],
        'name': 'admin_public',
        'is_public': True
    }).json()

    admin_private_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['admin']['token'],
        'name': 'admin_private1',
        'is_public': False
    }).json()

    owner_public_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['owner']['token'],
        'name': 'owner_public',
        'is_public': True
    }).json()

    owner_private_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['owner']['token'],
        'name': 'owner_private1',
        'is_public': False
    }).json()

    user_private_details = requests.post(f"{url}/channels/create", json={
        'token': initialise_user_data['user1']['token'],
        'name': 'private2',
        'is_public': False
    }).json()

    return {
        'admin_publ': admin_public_details,
        'admin_priv': admin_private_details,
        'owner_publ': owner_public_details,
        'owner_priv': owner_private_details,
        'user1_priv': user_private_details
    }

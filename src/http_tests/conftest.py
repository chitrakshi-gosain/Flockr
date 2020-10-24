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

@pytest.fixture()
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

    user4 = {
        'email': 'user4@email.com',
        'password': 'user4_pass1!',
        'name_first': 'user4_first',
        'name_last': 'user4_last'
    }

    user5 = {
        'email': 'user5@email.com',
        'password': 'user5_pass1!',
        'name_first': 'user5_first',
        'name_last': 'user5_last'
    }

    user6 = {
        'email': 'user6@email.com',
        'password': 'user6_pass1!',
        'name_first': 'user6_first',
        'name_last': 'user6_last'
    }

    user7 = {
        'email': 'user7@email.com',
        'password': 'user7_pass1!',
        'name_first': 'user7_first',
        'name_last': 'user7_last'
    }

    user8 = {
        'email': 'user8@email.com',
        'password': 'user8_pass1!',
        'name_first': 'user8_first',
        'name_last': 'user8_last'
    }

    user9 = {
        'email': 'user9@email.com',
        'password': 'user9_pass1!',
        'name_first': 'user9_first',
        'name_last': 'user9_last'
    }

    user10 = {
        'email': 'user10@email.com',
        'password': 'user10_pass1!',
        'name_first': 'user10_first',
        'name_last': 'user10_last'
    }

    user11 = {
        'email': 'user11@email.com',
        'password': 'user11_pass1!',
        'name_first': 'user11_first',
        'name_last': 'user11_last'
    }
    
    return {
        'admin_dict': admin,
        'owner_dict': owner,
        'user0_dict': user0,
        'user1_dict': user1,
        'user2_dict': user2,
        'user3_dict': user3,
        'user4_dict': user4,
        'user5_dict': user5,
        'user6_dict': user6,
        'user7_dict': user7,
        'user8_dict': user8,
        'user9_dict': user9,
        'user10_dict': user10,
        'user11_dict': user11,
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

    user4 = initialise_user_dictionary['user4_dict']
    user4_details = requests.post(f"{url}/auth/register", json=user4).json()

    user5 = initialise_user_dictionary['user5_dict']
    user5_details = requests.post(f"{url}/auth/register", json=user5).json()

    user6 = initialise_user_dictionary['user6_dict']
    user6_details = requests.post(f"{url}/auth/register", json=user6).json()

    user7 = initialise_user_dictionary['user7_dict']
    user7_details = requests.post(f"{url}/auth/register", json=user7).json()

    user8 = initialise_user_dictionary['user8_dict']
    user8_details = requests.post(f"{url}/auth/register", json=user8).json()

    user9 = initialise_user_dictionary['user9_dict']
    user9_details = requests.post(f"{url}/auth/register", json=user9).json()

    user10 = initialise_user_dictionary['user10_dict']
    user10_details = requests.post(f"{url}/auth/register", json=user10).json()

    user11 = initialise_user_dictionary['user11_dict']
    user11_details = requests.post(f"{url}/auth/register", json=user11).json()

    return {
        'admin': admin_details,
        'owner': owner_details,
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'user6': user6_details,
        'user7': user7_details,
        'user8': user8_details,
        'user9': user9_details,
        'user10': user10_details,
        'user11': user11_details,
    }


@pytest.fixture
def initialise_channel_data(url, initialise_user_data):
    '''
    creates 3 channels with descriptive data for testing
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
        'user1_priv': user_private_details,
    }

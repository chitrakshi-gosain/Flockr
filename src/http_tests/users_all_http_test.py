'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/users/all", methods=['GET']) return json.dumps({users})
-> APP.route("/auth/logout", methods=['POST']) return json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_users
'''

'''
EXCEPTIONS
Error type: AccessError
    -> Invalid token
'''

@pytest.fixture
def users_all_initialise_users(url):
    '''
    Sets up various user sample data for testing purposes
    '''

    # Register users:
    # Realistic test data
    john_details = requests.post(f'{url}/auth/register', json={
        'email': 'johnsmith@gmail.com',
        'password': 'qweRt1uiop!',
        'name_first': 'John',
        'name_last': 'Smith',
    }).json()
    jane_details = requests.post(f'{url}/auth/register', json={
        'email': 'janesmith@hotmail.com',
        'password': 'm3yDate0fb!rth',
        'name_first': 'Jane',
        'name_last': 'Smith',
    }).json()
    noah_details = requests.post(f'{url}/auth/register', json={
        'email': 'noah_navarro@yahoo.com',
        'password': 'aP00RP&ssWord1',
        'name_first': 'Noah',
        'name_last': 'Navarro',
    }).json()
    ingrid_details = requests.post(f'{url}/auth/register', json={
        'email': 'ingrid.cline@gmail.com',
        'password': '572o7563O*',
        'name_first': 'Ingrid',
        'name_last': 'Cline',
    }).json()
    donald_details = requests.post(f'{url}/auth/register', json={
        'email': 'donaldrichards@gmail.com',
        'password': 'kjDf2g@h@@df',
        'name_first': 'Donald',
        'name_last': 'Richards',
    }).json()

    # Returns user data that is implementation dependent (id, token)
    return {
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details,
        'donald': donald_details
    }

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_users_all_basic(url, users_all_initialise_users):
    '''
    Basic valid test case of users_all
    '''
    user_data = users_all_initialise_users

    all_users = requests.get(f'{url}/users/all', params={
        'token': user_data['john']['token'],
    }).json()

    exp_dict = {
        'users': [
            {
                'u_id': user_data['john']['u_id'],
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': user_data['jane']['u_id'],
                'email': 'janesmith@hotmail.com',
                'name_first': 'Jane',
                'name_last': 'Smith',
                'handle_str': 'janesmith',
            },
            {
                'u_id': user_data['noah']['u_id'],
                'email': 'noah_navarro@yahoo.com',
                'name_first': 'Noah',
                'name_last': 'Navarro',
                'handle_str': 'noahnavarro',
            },
            {
                'u_id': user_data['ingrid']['u_id'],
                'email': 'ingrid.cline@gmail.com',
                'name_first': 'Ingrid',
                'name_last': 'Cline',
                'handle_str': 'ingridcline',
            },
            {
                'u_id': user_data['donald']['u_id'],
                'email': 'donaldrichards@gmail.com',
                'name_first': 'Donald',
                'name_last': 'Richards',
                'handle_str': 'donaldrichards',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_logout(url, users_all_initialise_users):
    '''
    Tests that all user profiles are returned even if
    some users are logged out
    '''
    user_data = users_all_initialise_users

    requests.post(f'{url}/auth/logout', json={
        'token': user_data['jane']['token'],
    })
    requests.post(f'{url}/auth/logout', json={
        'token': user_data['donald']['token'],
    })

    all_users = requests.get(f'{url}/users/all', params={
        'token': user_data['john']['token'],
    }).json()

    exp_dict = {
        'users': [
            {
                'u_id': user_data['john']['u_id'],
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': user_data['jane']['u_id'],
                'email': 'janesmith@hotmail.com',
                'name_first': 'Jane',
                'name_last': 'Smith',
                'handle_str': 'janesmith',
            },
            {
                'u_id': user_data['noah']['u_id'],
                'email': 'noah_navarro@yahoo.com',
                'name_first': 'Noah',
                'name_last': 'Navarro',
                'handle_str': 'noahnavarro',
            },
            {
                'u_id': user_data['ingrid']['u_id'],
                'email': 'ingrid.cline@gmail.com',
                'name_first': 'Ingrid',
                'name_last': 'Cline',
                'handle_str': 'ingridcline',
            },
            {
                'u_id': user_data['donald']['u_id'],
                'email': 'donaldrichards@gmail.com',
                'name_first': 'Donald',
                'name_last': 'Richards',
                'handle_str': 'donaldrichards',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_invalid_token(url, users_all_initialise_users):
    '''
    Testing users_all with an invalid token parameter
    '''
    user_data = users_all_initialise_users

    invalid_token = user_data['john']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': user_data['john']['token'],
    })

    assert requests.get(f'{url}/users/all', params={
        'token': invalid_token
    }).status_code == 400
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
-> APP.route("/user/profile", methods=['GET']) return json.dumps({user})
-> APP.route("/auth/logout", methods=['POST']) return json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> User with u_id is not a valid user
Error type: AccessError
    -> Invalid token
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_user_profile_valid_own(url, initialise_user_data):
    '''
    Testing users checking their own profiles
    '''
    user_data = initialise_user_data

    profile_data = requests.get(f'{url}/user/profile', params={
        'token': user_data['user0']['token'],
        'u_id': user_data['user0']['u_id'],
    }).json()

    exp_dict = {
        'user': {
            'u_id': user_data['user0']['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las',
        }
    }

    assert profile_data == exp_dict

    profile_data = requests.get(f'{url}/user/profile', params={
        'token': user_data['user6']['token'],
        'u_id': user_data['user6']['u_id'],
    }).json()

    exp_dict = {
        'user': {
            'u_id': user_data['user6']['u_id'],
            'email': 'user6@email.com',
            'name_first': 'user6_first',
            'name_last': 'user6_last',
            'handle_str': 'user6_firstuser6_las',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_else(url, initialise_user_data):
    '''
    Testing users checking other user's profiles
    '''
    user_data = initialise_user_data

    profile_data = requests.get(f'{url}/user/profile', params={
        'token': user_data['user6']['token'],
        'u_id': user_data['user7']['u_id'],
    }).json()

    exp_dict = {
        'user': {
            'u_id': user_data['user7']['u_id'],
            'email': 'user7@email.com',
            'name_first': 'user7_first',
            'name_last': 'user7_last',
            'handle_str': 'user7_firstuser7_las',
        },
    }

    assert profile_data == exp_dict

    profile_data = requests.get(f'{url}/user/profile', params={
        'token': user_data['user7']['token'],
        'u_id': user_data['user9']['u_id'],
    }).json()

    exp_dict = {
        'user': {
            'u_id': user_data['user9']['u_id'],
            'email': 'user9@email.com',
            'name_first': 'user9_first',
            'name_last': 'user9_last',
            'handle_str': 'user9_firstuser9_las',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_logout(url, initialise_user_data):
    '''
    Testing the retrieval of profile data from a user that is logged out
    by a user that is logged in
    '''
    user_data = initialise_user_data

    requests.post(f'{url}/auth/logout', json={
        'token': user_data['user6']['token'],
    })

    profile_data = requests.get(f'{url}/user/profile', params={
        'token': user_data['user7']['token'],
        'u_id': user_data['user6']['u_id'],
    }).json()

    exp_dict = {
        'user': {
            'u_id': user_data['user6']['u_id'],
            'email': 'user6@email.com',
            'name_first': 'user6_first',
            'name_last': 'user6_last',
            'handle_str': 'user6_firstuser6_las',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_invalid_uid(url, initialise_user_data):
    '''
    Testing user_profile with an invalid u_id parameter
    '''
    user_data = initialise_user_data
    
    invalid_uid = -1

    assert requests.get(f'{url}/user/profile', params={
        'token': user_data['user7']['token'],
        'u_id': invalid_uid,
    }).status_code == 400

def test_user_profile_invalid_token(url, initialise_user_data):
    '''
    Testing user_profile with an invalid token parameter
    '''
    user_data = initialise_user_data

    invalid_token = user_data['user6']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    assert requests.get(f'{url}/user/profile', params={
        'token': invalid_token,
        'u_id': user_data['user7']['u_id'],
    }).status_code == 400
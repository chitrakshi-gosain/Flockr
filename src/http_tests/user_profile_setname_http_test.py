'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 2
'''

import json
import requests
import pytest
from error import InputError, AccessError

# need to plan how to format this
'''
****************************BASIC TEMPLATE******************************
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")


def test_http_user_profile_setname_no_errors(initialise_channel_data, initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    user_details = initialise_user_data['user0']
    token = user_details['token']
    u_id = user_details['u_id']
    name_first_old = user_details['name_first']
    name_last_old = user_details['name_last']

    user_profile_info = requests.get(f"{url}/user/profile", json={
        'token': token,
        'u_id': u_id
    }).json()
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    name_first_new = 'name_first_new'
    name_last_new = 'name_last_new'

    requests.post(f"{url}/user/profile/setname", json={
        'token': token,
        'name_first': name_first_new,
        'name_last': name_last_new
    }).json()

    user_profile_info = requests.get(f"{url}/user/profile", json={
        'token': token,
        'u_id': u_id
    }).json()
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_new
    assert user_dict['name_last'] == name_last_new


def test_http_user_profile_setname_inputerror(initialise_channel_data, initialise_user_data, url):
    '''
    test that user_profile_setname raises InputError
    if provided name_first or name_last is not between 1 and 50 characters in length
    '''

    user_details = initialise_user_data['user0']
    token = user_details['token']
    u_id = user_details['u_id']
    name_first_old = user_details['name_first']
    name_last_old = user_details['name_last']

    user_profile_info = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id
    }).json()
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    name_first_new = 'name_first_new'
    name_last_new = 'name_last_new'

    # Tests that auth_register raises an InputError when name_first is
    # less than 1 characters long
    name_first_new = ''
    with pytest.raises(InputError):
        requests.post(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': name_first_new,
            'name_last': name_last_new
        }).json()

    # Tests that auth_register raises an InputError when name_last is
    # less than 1 characters long
    name_first_new = 'name_first_new'
    name_last_new = ''
    with pytest.raises(InputError):
        requests.post(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': name_first_new,
            'name_last': name_last_new
        }).json()

    # Tests that auth_register raises an InputError when name_first is
    # more than 50 characters long
    name_last_new = 'name_last_new'
    name_first_new = '123456789012345678901234567890123456789012345678901'
    with pytest.raises(InputError):
        requests.post(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': name_first_new,
            'name_last': name_last_new
        }).json()

    # Tests that auth_register raises an InputError when name_last is
    # more than 50 characters long
    name_first_new = 'name_first_new'
    name_last_new = '123456789012345678901234567890123456789012345678901'
    with pytest.raises(InputError):
        requests.post(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': name_first_new,
            'name_last': name_last_new
        }).json()


def test_http_user_profile_setname_accesserror(initialise_user_data, url):
    '''
    test that user_profile_setname raises AccessError
    if provided token is invalid
    '''

    user_details = initialise_user_data['user0']
    token = user_details['token']
    u_id = user_details['u_id']
    name_first_old = user_details['name_first']
    name_last_old = user_details['name_last']

    user_profile_info = requests.get(f"{url}/user/profile", params={
        'token': token,
        'u_id': u_id
    }).json()
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    name_first_new = 'name_first_new'
    name_last_new = 'name_last_new'

    # assume ' ' is not a valid token
    token = " "

    with pytest.raises(AccessError):
        requests.post(f"{url}/user/profile/setname", json={
            'token': token,
            'name_first': name_first_new,
            'name_last': name_last_new
        }).json()

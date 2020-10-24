'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import json
import requests
import pytest

'''
**************************BASIC TEMPLATE****************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route(.....) return json.dumps({...})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> ...
'''

'''
EXCEPTIONS
Error type: InputError
    -> ..
Error type: AccessError
    -> ..
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")


def test_user_not_authorised(url, initialise_user_data, initialise_channel_data):
    user0 = initialise_user_data['user0']
    channel1_id = initialise_channel_data['user1_priv']
    response = requests.get(f"{url}/channel/details", params={
        'token': user0['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert response.status_code == 400

def test_channel_id_not_valid(url, initialise_user_data,):
    owner_credentials = initialise_user_data['owner']
    print(owner_credentials)
    invalid_channel_id = -1 

    response = requests.get(f"{url}/channel/details", params={
        'token': owner_credentials['token'],
        'channel_id': invalid_channel_id
    })
    assert response.status_code == 400


def test_token_invalid(url, initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['owner_priv']

    response = requests.get(f"{url}/channel/details", params={
        'token': 'incorrect_user_token',
        'channel_id': channel1_id['channel_id']
    })
    assert response.status_code == 400

def test_return_type(url, initialise_user_data, initialise_channel_data):
    user1_credentials = initialise_user_data['user1']      
    channel1_id = initialise_channel_data['owner_publ']
    join_response = requests.post(f"{url}/channel/join", json={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert join_response.status_code == 200

    details_response = requests.get(f"{url}/channel/details", params={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert details_response.status_code == 200
    details_payload = details_response.json()

    assert isinstance(details_payload, dict)

    assert isinstance(details_payload['name'], str)

    assert isinstance(details_payload['owner_members'], list)
    assert isinstance(details_payload['owner_members'][0], dict)
    assert isinstance(details_payload['owner_members'][0]['u_id'], int)
    assert isinstance(details_payload['owner_members'][0]['name_first'], str)
    assert isinstance(details_payload['owner_members'][0]['name_last'], str)

    assert isinstance(details_payload['all_members'], list)
    assert isinstance(details_payload['all_members'][0], dict)
    assert isinstance(details_payload['all_members'][0]['u_id'], int)
    assert isinstance(details_payload['all_members'][0]['name_first'], str)
    assert isinstance(details_payload['all_members'][0]['name_last'], str)

def test_channel_details_case(url, initialise_user_data, initialise_channel_data):

    owner_credentials = initialise_user_data['owner']
    user1_credentials = initialise_user_data['user1']      

    channel1_id = initialise_channel_data['owner_publ']
    join_response = requests.post(f"{url}/channel/join", json={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert join_response.status_code == 200

    details_response = requests.get(f"{url}/channel/details", params={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert details_response.status_code == 200
    details_payload = details_response.json()

    owner = {
        'u_id': owner_credentials['u_id'],
        'name_first': 'owner_first',
        'name_last': 'owner_last'
        }

    user1 = {
        'u_id': user1_credentials['u_id'],
        'name_first': 'user1_first',
        'name_last': 'user1_last'
        }

    channel_contents = {
        'name': 'owner_public',
        'owner_members': [owner],
        'all_members': [owner, user1]
        }

    assert channel_contents == details_payload

def test_channel_details_empty_channel(url, initialise_user_data, initialise_channel_data):
    admin_credentials = initialise_user_data['admin']
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_publ']

    leave_response = requests.post(f"{url}/channel/leave", json={
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert leave_response.status_code == 200

    details_response = requests.get(f"{url}/channel/details", params={
        'token': admin_credentials['token'],
        'channel_id': channel1_id['channel_id']
    })
    assert details_response.status_code == 200
    details_payload = details_response.json()

    channel_contents = {
        'name': 'owner_public',
        'owner_members': [],
        'all_members': []
        }

    assert channel_contents == details_payload
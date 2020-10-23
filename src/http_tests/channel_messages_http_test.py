'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import json
import requests
import pytest

'''
***************************BASIC TEMPLATE*****************************
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
    user1_credentials = initialise_user_data['user1']
    channel1_id = initialise_channel_data['owner_priv']
    response = requests.get(f"{url}/channel/messages", params={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert response.status_code == 400

def test_channel_id_not_valid(url, initialise_user_data):
    user1_credentials = initialise_user_data['user1']      
    invalid_channel_id = -1 

    response = requests.get(f"{url}/channel/messages", params={
        'token': user1_credentials['token'],
        'channel_id': invalid_channel_id,
        'start': 0
    })
    assert response.status_code == 400

def test_token_invalid(url, initialise_channel_data):
    channel1_id = initialise_channel_data['owner_priv']

    response = requests.get(f"{url}/channel/messages", params={
        'token': 'invalid_user_token',
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert response.status_code == 400

def test_return_type(url, initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    response = requests.get(f"{url}/channel/messages", params={
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    message_payload = response.json()
    print(message_payload)
    assert response.status_code == 200
    # we need to check the return type of message list after we implement send_message from message.py

    assert isinstance(message_payload['messages'], list)
    # assert isinstance(message_payload['messages'][0]['message_id'], int)
    # assert isinstance(message_payload['messages'][0]['u_id'], int)
    # assert isinstance(message_payload['messages'][0]['mesaage'], str)
    # assert isinstance(message_payload['messages'][0]['time_created'], time)

    assert isinstance(message_payload['start'], int)
    assert isinstance(message_payload['end'], int)

def test_empty_messages(url, initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_publ']
    response = requests.get(f"{url}/channel/messages", params={
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert response.status_code == 200
    message_payload = response.json()

    expected_message_history = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    assert expected_message_history == message_payload
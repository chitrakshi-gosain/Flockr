'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

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
-> APP.route("/message/send", methods=['POST']) return
    json.dumps({token, channel_id, message})
-> APP.route("/message/pin", methods=['POST']) return
    json.dumps({})
-> APP.route("/channel/join", methods=['POST']) return json.dumps({})
-> APP.route("/auth/register", methods=['POST']) return
    json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error Type: InputError
    -> token is invalid
    -> Message is already pinned
    -> message_id given is not a valid message_Id
Error Type: AccessError
    -> User is not an authorised member of the channel which contains the message
    -> The user is not an owner
'''
def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def get_messages(url, admin_token):
    messages = requests.get(url + "/search", params = {
        "token": admin_token,
        "query_str": ""
    }).json()
    return messages

def test_token_invalid(url, reset, initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']

    # send_message
    response = requests.post(url + "/message/send", json={
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'message': "Sample message" 
    })
    assert response.status_code == 200
    message1_id = response.json()

    # pin message
    send_input = {
        'token': 'incorrect_owner_token',
        'message_id': message1_id['message_id']
    }

    response = requests.post(url + "/message/pin", json=send_input)
    assert response.status_code == 400



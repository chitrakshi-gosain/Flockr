'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor -

Iteration 1
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> is_user_in_channel(url, user_id, token, channel_id) return amount of times u_id was found in channel
-> test_channel_join_basic()
-> test_channel_join_invalid_channel()
-> test_channel_join_private_user()
-> test_channel_join_private_admin()
-> test_channel_join_invalid_token()
-> test_channel_join_already_member()
'''

'''
----channel_join Documentation----
Parameters:
(token, channel_id)

Return Type:
{}

Exceptions:
    InputError (400) when:
        -> Channel ID is not a valid channel
    AccessError (400) when:
        -> channel_id refers to a channel that is private (when the authorised user is not a global owner)

Description: Given a channel_id of a channel that the
             authorised user can join, adds them to that channel
'''

def get_messages(url, admin_token):
    messages = requests.get(url + "/search", params = {
        "token": admin_token,
        "query_str": ""
    }).json()
    return messages

def test_user_not_authorised(url, reset, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['owner']['token']
    channel_id = initialise_channel_data['owner_priv']['channel_id']

    message_to_send = {
        'token': token,
        'channel_id': channel_id,
        'message': "Sample Message"
    }
    send_response = requests.post(f"{url}/message/send", json=message_to_send)
    assert send_response.status_code == 200
    send_payload = send_response.json()

    # should call channel messages for sanity check 
    remove_input = {
        "token": 'invalid_token',
        "message_id": send_payload['message_id']
    }
    response = requests.delete(url + "/message/remove", json=remove_input)
    assert response.status_code == 400

def test_token_invalid(url, initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel_id = initialise_channel_data['owner_priv']['channel_id']

    message_to_send = {
        'token': owner_credentials['token'],
        'channel_id': channel_id,
        'message': "Sample Message"
    }
    send_response = requests.post(f"{url}/message/send", json=message_to_send)
    assert send_response.status_code == 200
    send_payload = send_response.json()

    remove_input = {
        "token": 'invalid_token',
        "message_id": send_payload['message_id']
    }
    response = requests.delete(url + "/message/remove", json=remove_input)
    assert response.status_code == 400

def test_invalid_message_id(url, initialise_user_data, initialise_channel_data):
    
    owner_token = initialise_user_data['owner']['token']
    incorrect_message_id = -1
    remove_input = {
        "token": owner_token,
        "message_id": incorrect_message_id
    }
    response = requests.delete(url + "/message/remove", json=remove_input)
    assert response.status_code == 400


def test_empty(url, initialise_user_data, initialise_channel_data):
    
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']   
    
    message_to_send = {
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'message': "Sample Message"
    }
    send_response = requests.post(f"{url}/message/send", json=message_to_send)
    assert send_response.status_code == 200
    send_payload = send_response.json()

    remove_input = {
        "token": owner_credentials['token'],
        "message_id": send_payload['message_id']
    }
    response = requests.delete(url + "/message/remove", json=remove_input)
    assert response.status_code == 200

    messages_input = {
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    }
    
    message_response = requests.get(f"{url}/channel/messages", params=messages_input)
    assert message_response.status_code == 200
    message_payload = message_response.json()
    assert not message_payload['messages']

# add a integration test where message is sent and then successfully edited
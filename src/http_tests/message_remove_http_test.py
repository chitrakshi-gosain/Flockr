'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 1
'''

import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
-> APP.route("/channel/messages", methods=['GET']) return
    json.dumps({messages, start, end})
-> APP.route("/message/send", methods=['POST']) return
   json.dumps({token, channel_id, message})
-> APP.route("/message/remove", methods=['POST']) return
   json.dumps({token, message_id})
-> APP.route("/search", methods=['GET']) return
    json.dumps({messages})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error Type: InputError
    -> Channel ID is not a valid channel
Error Type: AccessError
    -> channel_id refers to a channel that is private (when the authorised user is not a global owner)
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

# # add a integration test where message is sent and then successfully edited
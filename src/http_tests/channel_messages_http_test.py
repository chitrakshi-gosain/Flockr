'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 2
'''

import requests

'''
***************************BASIC TEMPLATE*****************************
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
Error type: InputError
    -> Channel ID is not a valid channel
    -> start is greater than the total number of messages in the channel
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
    -> token is invalid
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''

    assert url.startswith("http")

def test_user_not_authorised(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_messages raises AccessError
    if user is not a member of channel with channel_id
    '''
    user1_credentials = initialise_user_data['user1']
    channel1_id = initialise_channel_data['owner_priv']
    response = requests.get(f"{url}/channel/messages", params={
        'token': user1_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert response.status_code == 400

def test_channel_id_not_valid(url, initialise_user_data):
    '''
    check that channel_messages raises InputError
    if Channel ID is not a valid channel
    '''
    user1_credentials = initialise_user_data['user1']
    invalid_channel_id = -1

    response = requests.get(f"{url}/channel/messages", params={
        'token': user1_credentials['token'],
        'channel_id': invalid_channel_id,
        'start': 0
    })
    assert response.status_code == 400

def test_token_invalid(url, initialise_channel_data):
    '''
    check that channel_messages raises AccessError
    if token is invalid
    '''
    channel1_id = initialise_channel_data['owner_priv']

    response = requests.get(f"{url}/channel/messages", params={
        'token': 'invalid_user_token',
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert response.status_code == 400

def test_return_type(url, initialise_user_data, initialise_channel_data):
    '''
    checks that channel_messages returns objects of the correct data types
    '''
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']

    send_input = {
        "token": owner_credentials['token'],
        "channel_id": channel1_id['channel_id'],
        "message": "Sample message"
    }
    send_response = requests.post(url + "/message/send", json=send_input)
    assert send_response.status_code == 200

    message_response = requests.get(f"{url}/channel/messages", params={
        'token': owner_credentials['token'],
        'channel_id': channel1_id['channel_id'],
        'start': 0
    })
    assert message_response.status_code == 200
    message_payload = message_response.json()
    print(message_payload)

    assert isinstance(message_payload['messages'], list)
    assert isinstance(message_payload['messages'][0]['message_id'], int)
    assert isinstance(message_payload['messages'][0]['u_id'], int)
    assert isinstance(message_payload['messages'][0]['message'], str)
    assert isinstance(message_payload['messages'][0]['time_created'], int)

    assert isinstance(message_payload['start'], int)
    assert isinstance(message_payload['end'], int)

def test_empty_messages(url, initialise_user_data, initialise_channel_data):
    '''
    checks that start == 0 and end == -1 if no messages have been sent
    '''
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

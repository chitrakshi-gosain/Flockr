'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
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
-> APP.route("/search") return json.dumps({messages})
-> APP.route("/message/send") return json.dumps({})
-> APP.route("/channel/join") return json.dumps({})
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
Error type: AccessError
    -> Invalid token
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def is_message_in_messages(message_str, messages):
    for message in messages['messages']:
        if message['message'] == message_str:
            return True
    return False

def test_search_not_in_channels(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message_str = "I am in no channels"
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": message_str
    }
    requests.post(url + "/message/send", json=message_input)

    search_input = {
        "token": token,
        "query_str": "I am in no channels"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    assert response.json() == {"messages": []}

def test_search_join_channel(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #message1 stuff
    message1_str = 'I am in no channels'
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": message1_str
    }
    requests.post(url + "/message/send", json=message_input)

    #search
    search_input = {
        "token": token,
        "query_str": "channel"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    assert response.json() == {"messages": []}

    #join channel
    requests.post(url + "/channel/join", json={
        "token": token,
        "channel_id": channel_id
    })

    #message2 stuff
    message2_str = "Now Im in a channel"
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": message2_str
    }
    requests.post(url + "/message/send", json=message_input)

    #seach again
    search_input = {
        "token": token,
        "query_str": "no channel"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    assert is_message_in_messages(message1_str, searched_messages)
    assert not is_message_in_messages(message2_str, searched_messages)

def test_search_no_messages(url, initialise_user_data, initialise_channel_data):

    search_input = {
        "token": initialise_user_data['user1']['token'],
        "query_str": "There are no messages"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    assert response.json() == { 'messages': [] }

def test_search_empty_query(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #user1 join channel
    requests.post(url + "/channel/join", json={
        "token": token,
        "channel_id": channel_id
    })

    #message1 stuff
    message1_str = "this is message1"
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": message1_str
    }
    requests.post(url + "/message/send", json=message_input)

    #message2 stuff
    message2_str = "this is message2"
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": message2_str
    }
    requests.post(url + "/message/send", json=message_input)

    #search
    search_input = {
        "token": initialise_user_data['user1']['token'],
        "query_str": ""
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    assert is_message_in_messages(message1_str, searched_messages)
    assert is_message_in_messages(message2_str, searched_messages)

def test_search_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['user1_priv']['channel_id']

    #message stuff
    message_str = 'private'
    message_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": channel_id,
        "message": message_str
    }
    requests.post(url + "/message/send", json=message_input).json()

    #search
    search_input = {
        "token": token,
        "query_str": "priv"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    assert is_message_in_messages(message_str, searched_messages)

def test_search_multiple_channels(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']

    #message1
    message1_str = 'channel1'
    message_input = {
        "token": token,
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": message1_str
    }
    requests.post(url + "/message/send", json=message_input).json()

    #message2
    message2_str = 'channel2'
    message_input = {
        "token": token,
        "channel_id": initialise_channel_data['admin_priv']['channel_id'],
        "message": message2_str
    }
    requests.post(url + "/message/send", json=message_input).json()

    #search
    search_input = {
        "token": token,
        "query_str": "channel"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    assert is_message_in_messages(message1_str, searched_messages)
    assert is_message_in_messages(message2_str, searched_messages)

def test_search_invalid_token(url, initialise_user_data, initialise_channel_data):

    search_input = {
        "token": ' ',
        "query_str": "This should be illegal"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 400

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

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

# def test_url(url):
#     '''
#     A simple sanity test to check that the server is set up properly
#     '''
#     assert url.startswith("http")

def pop_datetimes(messages):
    for entry in messages:
        entry.pop('time_created')
    return messages

def test_search_not_in_channels(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": "I am in no channels"
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
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": "I am in no channels"
    }
    message1 = requests.post(url + "/message/send", json=message_input).json()
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'I am in no channels',
    }
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
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": "Now Im in a channel"
    }
    message2 = requests.post(url + "/message/send", json=message_input).json()
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'Now Im in a channel',
    }
    #seach again
    search_input = {
        "token": token,
        "query_str": "no channel"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info not in popped

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
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": "this is message1"
    }
    message1 = requests.post(url + "/message/send", json=message_input).json()
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'this is message1',
    }

    #message2 stuff
    message_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": channel_id,
        "message": "this is message2"
    }
    message2 = requests.post(url + "/message/send", json=message_input).json()
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'this is message2',
    }

    #search
    search_input = {
        "token": initialise_user_data['user1']['token'],
        "query_str": ""
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    popped =  pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_search_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['user1_priv']['channel_id']

    #message stuff
    message_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": channel_id,
        "message": "private"
    }
    message = requests.post(url + "/message/send", json=message_input).json()
    message_info = {
        'message_id' : message['message_id'],
        'u_id' : initialise_user_data['user1']['u_id'],
        'message' : 'private',
    }

    #search
    search_input = {
        "token": token,
        "query_str": "priv"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    popped = pop_datetimes(searched_messages['messages'])
    assert message_info in popped

def test_search_multiple_channels(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']

    #message1
    message_input = {
        "token": token,
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "channel1"
    }
    message1 = requests.post(url + "/message/send", json=message_input).json()
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'channel1',
    }

    #message2
    message_input = {
        "token": token,
        "channel_id": initialise_channel_data['admin_priv']['channel_id'],
        "message": "channel2"
    }
    message2 = requests.post(url + "/message/send", json=message_input).json()
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : initialise_user_data['admin']['u_id'],
        'message' : 'channel2',
    }

    #search
    search_input = {
        "token": token,
        "query_str": "channel"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 200
    searched_messages = response.json()

    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_search_invalid_token(url, initialise_user_data, initialise_channel_data):

    search_input = {
        "token": ' ',
        "query_str": "This should be illegal"
    }
    response = requests.get(url + "/search", params=search_input)
    assert response.status_code == 400

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 2
'''

import json
import requests
import pytest
import helper
from error import InputError, AccessError

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

# def test_something(url):
#     '''
#     ADD DOCSTRING HERE
#     '''

def test_http_message_edit_noerrors(initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    user = {
        'email': 'user@email.com',
        'password': 'user_pass1!',
        'name_first': 'user_first',
        'name_last': 'user_last'
    }

    user_details = requests.post(f"{url}/auth/register", json=user).json()
    token = user_details['token']

    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token,
        'name': "A Channel Name",
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_info = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    }).json()
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    requests.post(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': second_message
    })

    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == second_message

def test_http_message_edit_secondmessage(initialise_user_data, url):
    '''
    edits the second sent message, not the first
    '''

    user = {
        'email': 'user@email.com',
        'password': 'user_pass1!',
        'name_first': 'user_first',
        'name_last': 'user_last'
    }

    user_details = requests.post(f"{url}/auth/register", json=user).json()
    token = user_details['token']

    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token,
        'name': "A Channel Name",
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    first_message0 = "This is the first original message."
    first_message1 = "This is the second original message."

    message_info0 = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message0
    })
    message_id0 = message_info0["message_id"]
    message_dict0 = helper.get_message_info(message_id0)
    assert message_dict0['message'] == first_message0

    message_info1 = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message1
    })
    message_id1 = message_info1["message_id"]
    message_dict1 = helper.get_message_info(message_id1)
    assert message_dict1['message'] == first_message1

    second_message1 = "This is the second edited message."

    requests.post(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id1,
        'message': second_message1
    })
    message_dict1 = helper.get_message_info(message_id1)
    assert message_dict1['message'] == second_message1

def test_http_message_edit_emptystring(initialise_user_data, url):
    '''
    test that message_edit deletes the message
    if provided with an empty string
    '''

    user = {
        'email': 'user@email.com',
        'password': 'user_pass1!',
        'name_first': 'user_first',
        'name_last': 'user_last'
    }

    user_details = requests.post(f"{url}/auth/register", json=user).json()
    token = user_details['token']

    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token,
        'name': "A Channel Name",
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_info = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    }).json()
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = ""

    requests.post(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': second_message
    })

    # get_message_from_id returns False if message does not exist
    # therefore check that message has been deleted
    message_dict = helper.get_message_info(message_id)
    assert not message_dict

def test_http_message_edit_notsender(initialise_user_data, url):
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    token0 = user0_details['token']

    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()
    token1 = user1_details['token']

    # user0 creates channel, user1 joins it
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': "A Channel Name",
        'is_public': True
    }).json()
    channel_id = channel_info["channel_id"]

    requests.post(f"{url}/channel/join", json={
        'token': token1,
        'channel_id': channel_id
    })

    first_message = "This is the original message."

    message_info = requests.post(f"{url}/message/send", json={
        'token': token0,
        'channel_id': channel_id,
        'message': first_message
    }).json()

    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    with pytest.raises(AccessError):
        requests.post(f"{url}/message/edit", json={
            'token': token1,
            'message_id': message_id,
            'message': second_message
        })

def test_http_message_edit_notauth(initialise_user_data, url):
    '''
    test that message_edit raises AccessError
    if token is not authorised
    i.e. user is not admin of the flockr or owner of the channel message is in
    '''

    user = {
        'email': 'user@email.com',
        'password': 'user_pass1!',
        'name_first': 'user_first',
        'name_last': 'user_last'
    }

    user_details = requests.post(f"{url}/auth/register", json=user).json()
    token = user_details['token']

    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token,
        'name': "A Channel Name",
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_info = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    }).json()
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    # assume " " is not a valid token
    token = " "

    with pytest.raises(AccessError):
        requests.post(f"{url}/message/edit", json={
            'token': token,
            'message_id': message_id,
            'message': second_message
        })

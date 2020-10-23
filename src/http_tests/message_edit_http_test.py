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

def test_http_message_edit_noerrors(initialise_channel_data, initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
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

def test_http_message_edit_secondmessage(initialise_channel_data, initialise_user_data, url):
    '''
    edits the second sent message, not the first
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
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

def test_http_message_edit_emptystring(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit deletes the message
    if provided with an empty string
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
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

def test_http_message_edit_notsender(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    token_admin = admin['token']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    u_id0, token0 = user0['u_id'], user0['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user0 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })

    first_message = "This is the original message."

    message_info = requests.post(f"{url}/message/send", json={
        'token': token_admin,
        'channel_id': channel_id,
        'message': first_message
    }).json()

    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    with pytest.raises(AccessError):
        requests.post(f"{url}/message/edit", json={
            'token': token0,
            'message_id': message_id,
            'message': second_message
        })

def test_http_message_edit_notauth(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit raises AccessError
    if token is not authorised
    i.e. user is not admin of the flockr or owner of the channel message is in
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
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

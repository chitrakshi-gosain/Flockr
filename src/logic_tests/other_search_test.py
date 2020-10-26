'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
'''

import pytest
from error import InputError, AccessError
from other import search
from message import message_send
from channel import channel_join

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> channel_join(token, channel_id) return {}
-> search(token, query_str) return {messages}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
'''

def pop_datetimes(messages):
    for entry in messages:
        entry.pop('time_created')
    return messages

def test_other_search_not_in_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message_send(users['admin']['token'], channel_id, 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_join_channel(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message1 = message_send(users['admin']['token'], channel_id, 'I am in no channels')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'I am in no channels',
    }

    assert search(users['user0']['token'], 'channel') == { 'messages': [] }

    channel_join(users['user0']['token'], channel_id)

    message2 = message_send(users['admin']['token'], channel_id, 'Now Im in a channel')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'Now Im in a channel',
    }

    searched_messages = search(users['user0']['token'], 'no channels')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info not in popped

def test_other_search_no_messages(initialise_user_data):
    users = initialise_user_data

    assert search(users['user0']['token'], 'There are no messages') == { 'messages': [] }

def test_other_search_empty_query(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['user0']['token'], channel_id)

    message1 = message_send(users['admin']['token'], channel_id, 'this is message1')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message1',
    }

    message2 = message_send(users['admin']['token'], channel_id, 'this is message2')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message2',
    }

    searched_messages = search(users['user0']['token'], '')
    popped =  pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_other_search_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['user0_priv']['channel_id']

    message1 = message_send(users['user0']['token'], channel_id, 'private')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['user0']['u_id'],
        'message' : 'private',
    }

    searched_messages = search(users['admin']['token'], 'priv')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped

def test_other_search_multiple_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id1 = initialise_channel_data['admin_publ']['channel_id']
    channel_id2 = initialise_channel_data['admin_priv']['channel_id']

    message1 = message_send(users['admin']['token'], channel_id1, 'channel1')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'channel1',
    }

    message2 = message_send(users['admin']['token'], channel_id2, 'channel2')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'channel2',
    }

    searched_messages = search(users['admin']['token'], 'channel')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_other_search_invalid_token(reset):
    invalid_token = ' '

    with pytest.raises(AccessError):
        search(invalid_token, 'This should be illegal')

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

def is_message_in_messages(message_str, messages):
    for message in messages['messages']:
        if message['message'] == message_str:
            return True
    return False

def test_other_search_not_in_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message_send(users['admin']['token'], channel_id, 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_join_channel(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message1_str = 'I am in no channels'
    message_send(users['admin']['token'], channel_id, message1_str)

    assert search(users['user0']['token'], 'channel') == { 'messages': [] }

    channel_join(users['user0']['token'], channel_id)

    message2_str = 'Now Im in a channel'
    message_send(users['admin']['token'], channel_id, message2_str)

    searched_messages = search(users['user0']['token'], 'no channels')

    assert is_message_in_messages(message1_str, searched_messages)
    assert not is_message_in_messages(message2_str, searched_messages)

def test_other_search_no_messages(initialise_user_data):
    users = initialise_user_data

    assert search(users['user0']['token'], 'There are no messages') == { 'messages': [] }

def test_other_search_empty_query(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['user0']['token'], channel_id)

    message1_str = 'this is message1'
    message_send(users['admin']['token'], channel_id, message1_str)

    message2_str = 'this is message2'
    message_send(users['admin']['token'], channel_id, message2_str)

    searched_messages = search(users['user0']['token'], '')

    assert is_message_in_messages(message1_str, searched_messages)
    assert is_message_in_messages(message2_str, searched_messages)

def test_other_search_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['user0_priv']['channel_id']

    message1_str = 'private'
    message_send(users['user0']['token'], channel_id, message1_str)

    searched_messages = search(users['admin']['token'], 'priv')

    assert is_message_in_messages(message1_str, searched_messages)

def test_other_search_multiple_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id1 = initialise_channel_data['admin_publ']['channel_id']
    channel_id2 = initialise_channel_data['admin_priv']['channel_id']

    message1_str = 'channel1'
    message_send(users['admin']['token'], channel_id1, message1_str)

    message2_str = 'channel2'
    message_send(users['admin']['token'], channel_id2, message2_str)

    searched_messages = search(users['admin']['token'], 'channel')

    assert is_message_in_messages(message1_str, searched_messages)
    assert is_message_in_messages(message2_str, searched_messages)

def test_other_search_invalid_token(reset):
    invalid_token = ' '

    with pytest.raises(AccessError):
        search(invalid_token, 'This should be illegal')

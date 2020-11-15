'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 2
'''

import pytest
from channel import channel_messages
from message import message_send, message_remove
from other import search
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, firstname, lastname)
-> channels_create(token) return {channel_id}
-> message_send(token, channel_id, message) return {messag
-> channel_messages(token, channel_id, start) return
   {messages, start, end}e_id}
-> message_remove(token, message_id) return {}
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
Error type: InputError
    -> Channel ID is not a valid channel
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
'''

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages

def test_user_not_authorised(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    user1_credentials = initialise_user_data['user1']

    with pytest.raises(AccessError):
        message_remove(user1_credentials['token'], message_id['message_id'])


def test_token_invalid(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")

    with pytest.raises(AccessError):
        message_remove('incorrect_user1_token', message_id['message_id'])

def test_invalid_message_id(initialise_user_data, initialise_channel_data):

    owner_credentials = initialise_user_data['owner']
    incorrect_message_id = -1
    with pytest.raises(InputError):
        message_remove(owner_credentials['token'], incorrect_message_id)

def test_empty(initialise_user_data, initialise_channel_data):

    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']                        # create a public channel
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    message_remove(owner_credentials['token'], message_id['message_id'])

    messages_history = channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0)
    assert messages_history['messages'] == []

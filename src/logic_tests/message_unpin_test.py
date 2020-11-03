'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 2
'''

import pytest
from channel import channel_join
from message import message_pin, message_unpin
from other import search
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, firstname, lastname)
-> channels_create(token) return {channel_id}
-> message_pin(token, message_id) return {}
-> message_unpin(token, message_id) return {}
-> message_send(token, channel_id, message) return {message_id}
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
    -> token passed in is not a valid token
    -> message_id is not a valid message
    -> Message with ID message_id is already pinned
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
    -> Authorised user is not an owner of the channel
'''
'''
message_id is not a valid message
Message with ID message_id is already pinned
'''

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages

def test_token_invalid(initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    message1_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Message to be pinned.")

    with pytest.raises(AccessError):
        message_pin('incorrect_user1_token', message1_id['message_id'])

def test_invalid_message_id(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    incorrect_message_id = -1
    with pytest.raises(InputError):
        message_pin(owner_credentials['token'], incorrect_message_id)

def test_message_already_unpinned(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    message1_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Message to be pinned.")
    with pytest.raises(InputError):
        message_unpin(token, message1_id['message_id'])


def test_user_not_authorised(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    user1_credentials = initialise_user_data['user1']  
    channel1_id = initialise_channel_data['owner_priv']
    message1_id = message_send(user1_credentials['token'], channel1_id['channel_id'], "First message in this channel.")

    with pytest.raises(AccessError):
        message_unpin(owner_credentials['token'], message1_id['message_id'])

def test_user_not_owner():
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_priv']
    message1_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "First message in this channel.")
    user1_credentials = initialise_user_data['user1']
    with pytest.raises(AccessError):
        message_unpin(user1_credentials['token'], message1_id['message_id'])

def test_sample_case():
    admin_credentials = initialise_user_data['admin']
    channel1_id = initialise_channel_data['admin_priv']

    message1_id = message_send(admin_credentials['token'], channel1_id['channel_id'], "The date for the AGM is 14th of November, 2020")
    message_pin(owner_credentials['token'], message1_id['message_id'])

    messages = get_messages(admin_credentials['token'])
    for message in messages:
        if message['message_id'] == message1_id['message_id']:
            assert message['is_pinned'] == True
            
    message_unpin(owner_credentials['token'], message1_id['message_id'])
    messages = get_messages(admin_credentials['token'])
    for message in messages:
        if message['message_id'] == message1_id['message_id']:
            assert message['is_pinned'] == False







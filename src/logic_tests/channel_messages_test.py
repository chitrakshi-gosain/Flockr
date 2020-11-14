'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 1
'''

import pytest
from channel import channel_messages
from message import message_send
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channel_messages(token, channel_id, start) return
   {messages, start, end}
-> channels_create(token, name. is_public) return {channel_id}
-> channel_join(token, channel_id) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS:
InputError when:
    -> Channel ID is not a valid channel
AccessError when:
    -> channel_id refers to a channel that is private (when the
        authorised user is not a global owner
'''

def test_user1_not_authorised(initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['owner_priv']
    user1_credentials = initialise_user_data['user1']
    with pytest.raises(AccessError):
        channel_messages(user1_credentials['token'], channel1_id['channel_id'], 0)

def test_channel_id_not_valid(initialise_user_data):
    user1_credentials = initialise_user_data['user1']
    invalid_channel_id = -1

    with pytest.raises(InputError):
        channel_messages(user1_credentials['token'], invalid_channel_id, 0)

def test_token_invalid(initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['owner_priv']
    with pytest.raises(AccessError):
        channel_messages('incorrect_user1_token', channel1_id['channel_id'], 0)

def test_return_type(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel_id = initialise_channel_data['owner_priv']
    message_send(owner_credentials['token'], channel_id['channel_id'], "This is owner's channel")
    message_history = channel_messages(owner_credentials['token'], channel_id['channel_id'], 0)

    assert isinstance(message_history['messages'], list)
    assert isinstance(message_history['messages'][0]['message_id'], int)
    assert isinstance(message_history['messages'][0]['u_id'], int)
    assert isinstance(message_history['messages'][0]['message'], str)
    assert isinstance(message_history['messages'][0]['time_created'], int)
    assert isinstance(message_history['start'], int)
    assert isinstance(message_history['end'], int)

def test_empty_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_publ']

    messages_history = {'messages': [], 'start': 0, 'end': -1}
    assert (messages_history == channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0))

def test_start_more_than_total_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel_id = initialise_channel_data['owner_priv']
    with pytest.raises(InputError):
        channel_messages(owner_credentials['token'], channel_id['channel_id'], 2)

def test_50_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel_id = initialise_channel_data['owner_priv']

    #send the messages
    for i in range(55):
        message_send(owner_credentials['token'], channel_id['channel_id'], f"message {i}")

    messages_info = channel_messages(owner_credentials['token'], channel_id['channel_id'], 0)
    assert messages_info['end'] == 50

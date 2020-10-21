'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - 

Iteration 1
'''

import pytest
from auth import auth_register
from channel import channel_messages
from channels import channels_create
from other import clear
from error import InputError
from error import AccessError

def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        channel_messages(None, None, None)
        
def test_user1_not_authorised():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1
    with pytest.raises(AccessError):
        channel_messages(user1_credentials['token'], channel1_id['channel_id'], 0)


def test_channel_id_not_valid():

    clear()
    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1
    invalid_channel_id = -1
    with pytest.raises(InputError):
        channel_messages(user1_credentials['token'], invalid_channel_id, 0)

def test_token_invalid():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner

    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

    with pytest.raises(AccessError):
        channel_messages('incorrect_user1_token', channel1_id['channel_id'], 0)

def test_start_too_big():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

    with pytest.raises(InputError):
        channel_messages(owner_credentials['token'], channel1_id['channel_id'], 4)

def test_return_type():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel

    message_history = channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0)
    # we need to check the return type of message list after we implement send_message from message.py

    assert isinstance(message_history['messages'], list)
    assert isinstance(message_history['start'], int)
    assert isinstance(message_history['end'], int)

def test_empty_messages():
    clear()

    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel

    messages_history = {'messages': [], 'start': 0, 'end': -1}
    assert (messages_history == channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0))

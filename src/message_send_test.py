from auth import auth_register
from channel import channel_messages, channel_details
from channels import channels_create
from message import message_send
import data
import pytest
from other import clear
from error import InputError
from error import AccessError

def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        message_send(None, None, None)

def test_user_not_authorised():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1
    with pytest.raises(AccessError):
        message_send(user1_credentials['token'], channel1_id['channel_id'], "Sample message")


def test_channel_id_not_valid():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner

    invalid_channel_id = -1 
    with pytest.raises(InputError):
        message_send(owner_credentials['token'], invalid_channel_id, "Sample message")


def test_token_invalid():
    clear()

    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)
    with pytest.raises(AccessError):
        message_send('incorrect_user1_token', channel1_id['channel_id'], "Sample message")

def test_return_type():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel

    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    assert isinstance(message_id, dict)
    assert isinstance(message_id['message_id'], int)
    assert isinstance(data.data['messages']['message'][0], str)

def test_sample():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    assert data.data['messages']['message'][0] == "Sample message"





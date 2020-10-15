import pytest
from auth import auth_register
from channels import channels_create
from message import message_send, message_remove
import data
from other import clear
from error import InputError, AccessError

def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        message_remove(None, None)

def test_user_not_authorised():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")

    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

    with pytest.raises(AccessError):
        message_remove(user1_credentials['token'], message_id['message_id'])


def test_token_invalid():
    clear()

    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")

    with pytest.raises(AccessError):
        message_remove('incorrect_user1_token', message_id['message_id'])

def test_sample():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    message_remove(owner_credentials['token'], message_id['message_id'])
    assert data.data['messages'] == []
    
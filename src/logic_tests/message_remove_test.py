import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from message import message_send, message_remove
from other import clear, search
from error import InputError, AccessError

@pytest.fixture
def reset():
    clear()

@pytest.fixture
def initialise_user_data(reset):
    owner_details = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')   
    user1_details = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')      

    return {
        'owner': owner_details,
        'user1': user1_details
    }

@pytest.fixture
def initialise_channel_data(initialise_user_data):
    owner_credentials = initialise_user_data['owner']
    public_channel = channels_create(owner_credentials['token'], 'channel1_name', True)
    private_channel = channels_create(owner_credentials['token'], 'channel1_name', False)
    return {
        'public': public_channel,
        'private': private_channel
    }

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages

def test_user_not_authorised(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['private']
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    user1_credentials = initialise_user_data['user1']      

    with pytest.raises(AccessError):
        message_remove(user1_credentials['token'], message_id['message_id'])


def test_token_invalid(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['private']
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
    channel1_id = initialise_channel_data['private']                              # create a public channel
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    message_remove(owner_credentials['token'], message_id['message_id'])

    messages_history = channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0)
    assert messages_history['messages'] == []


from auth import auth_register
from channel import channel_messages
from channels import channels_create
import pytest
from other import clear
from error import InputError
from error import AccessError

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

def test_insufficient_parameters(reset):
    with pytest.raises(InputError):
        channel_messages(None, None, None)

def test_user1_not_authorised(initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['private']
    user1_credentials = initialise_user_data['user1']      
    with pytest.raises(AccessError):
        channel_messages(user1_credentials['token'], channel1_id['channel_id'], 0)

    
def test_channel_id_not_valid(initialise_user_data):

    user1_credentials = initialise_user_data['user1']      
    invalid_channel_id = -1 

    with pytest.raises(InputError):
        channel_messages(user1_credentials['token'], invalid_channel_id, 0)

def test_token_invalid(initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['private']
    with pytest.raises(AccessError):
        channel_messages('incorrect_user1_token', channel1_id['channel_id'], 0)

def test_return_type(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['private']
    message_history = channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0)
    # we need to check the return type of message list after we implement send_message from message.py

    assert isinstance(message_history['messages'], list)
    assert isinstance(message_history['start'], int)
    assert isinstance(message_history['end'], int)

def test_empty_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['public']

    messages_history = {'messages': [], 'start': 0, 'end': -1}
    assert (messages_history == channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0))


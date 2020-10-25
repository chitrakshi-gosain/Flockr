from auth import auth_register
from channel import channel_messages
from channels import channels_create
from message import message_send
import pytest
from other import clear
from error import InputError
from error import AccessError
from datetime import time

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
    channel_id = initialise_channel_data['private']
    message_send(owner_credentials['token'], channel_id['channel_id'], "This is owner's channel")
    message_history = channel_messages(owner_credentials['token'], channel_id['channel_id'], 0)

    assert isinstance(message_history['messages'], list)
    assert isinstance(message_history['messages'][0]['message_id'], int)
    assert isinstance(message_history['messages'][0]['u_id'], int)
    assert isinstance(message_history['messages'][0]['message'], str)
    # assert isinstance(message_history['messages'][0]['time_created'], time)
    assert isinstance(message_history['start'], int)
    assert isinstance(message_history['end'], int)

def test_empty_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['public']

    messages_history = {'messages': [], 'start': 0, 'end': -1}
    assert (messages_history == channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0))

def test_start_more_than_total_messages(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']
    channel_id = initialise_channel_data['private']
    with pytest.raises(InputError):
        channel_messages(owner_credentials['token'], channel_id['channel_id'], 2)

def test_channel_messages_50_messages(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['owner']['token']
    channel_id = initialise_channel_data['public']['channel_id']

    for i in range(50):
        message_send(token, channel_id, str(i))

    messages = channel_messages(token, channel_id, 0)
    assert message['end'] == 50

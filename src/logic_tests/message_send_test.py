from auth import auth_register
from channel import channel_join
from channels import channels_create
from message import message_send
import data
import pytest
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

def test_insufficient_parameters(reset):
    with pytest.raises(InputError):
        message_send(None, None, None)

def test_user_not_authorised(initialise_user_data, initialise_channel_data):

    channel1_id = initialise_channel_data['private']
    user1_credentials = initialise_user_data['user1']      
    with pytest.raises(AccessError):
        message_send(user1_credentials['token'], channel1_id['channel_id'], "Sample message")


def test_channel_id_not_valid(initialise_user_data):
    owner_credentials = initialise_user_data['owner']
    invalid_channel_id = -1
    with pytest.raises(InputError):
        message_send(owner_credentials['token'], invalid_channel_id, "Sample message")


def test_token_invalid(initialise_channel_data):

    channel1_id = initialise_channel_data['private']
    with pytest.raises(AccessError):
        message_send('incorrect_user1_token', channel1_id['channel_id'], "Sample message")

def test_return_type(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']

    channel1_id = initialise_channel_data['private']
    message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")

    admin_token = owner_credentials['token']
    messages = get_messages(admin_token)
    assert isinstance(messages['messages'], list)
    assert isinstance(messages['messages'][0], dict)
    assert isinstance(messages['messages'][0]['message_id'], int)
    assert isinstance(messages['messages'][0]['u_id'], int)
    assert isinstance(messages['messages'][0]['message'], str)
    assert isinstance(messages['messages'][0]['message'], object)

def test_sample(initialise_user_data, initialise_channel_data):
    
    channel1_id = initialise_channel_data['private']
    owner_credentials = initialise_user_data['owner']
    user1_credentials = initialise_user_data['user1']      

    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel
    channel_join(user1_credentials['token'], channel1_id['channel_id'])

    message_send(owner_credentials['token'], channel1_id['channel_id'], "Hey, how are you")
    message_id = message_send(user1_credentials['token'], channel1_id['channel_id'], "Good thank you, how are you!")
    message_send(owner_credentials['token'], channel1_id['channel_id'], "Very well, thanks.")

    admin_token = owner_credentials['token']
    messages = get_messages(admin_token)
    for message in messages['messages']:
        if message['message_id'] == message_id['message_id']:
            assert message['message'] == "Good thank you, how are you!"

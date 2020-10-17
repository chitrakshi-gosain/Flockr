import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from message import message_send, message_remove
from other import clear, search
from error import InputError, AccessError

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages
     
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

def test_empty():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)                                 # create a public channel
    message_id = message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")
    message_remove(owner_credentials['token'], message_id['message_id'])

    messages_history = channel_messages(owner_credentials['token'], channel1_id['channel_id'], 0)
    assert messages_history['messages'] == []

    

def test_multiple_dicts():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1

    admin_token = owner_credentials['token']
    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')
    
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel
    channel_join(user1_credentials['token'], channel1_id['channel_id'])
    
    message_send(user1_credentials['token'], channel1_id['channel_id'], "Mum, there's something I need to tell you")
    message_send(owner_credentials['token'], channel1_id['channel_id'], "What is it?")
    message_id = message_send(user1_credentials['token'], channel1_id['channel_id'], "I failed my assignment")
    messages = get_messages(admin_token)
    assert messages['messages'][2]['message'] == "I failed my assignment"

    message_remove(user1_credentials['token'], message_id['message_id'])
    message_send(owner_credentials['token'], channel1_id['channel_id'], "Sorry hunny I missed that. What did you delete?")
    message_send(user1_credentials['token'], channel1_id['channel_id'], "Oh it's nothing, I'll be home soon! Byee")
    message_send(user1_credentials['token'], channel1_id['channel_id'], "Bye son")

    # Check to see if the message has been deleted in the channel
    messages = get_messages(admin_token)
    assert messages['messages'][2]['message'] == "Sorry hunny I missed that. What did you delete?"

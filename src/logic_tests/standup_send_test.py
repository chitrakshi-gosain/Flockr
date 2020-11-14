'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

Iteration 3
'''

import time
import pytest
from error import AccessError, InputError
from standup import standup_start, standup_active, standup_send
from channel import channel_join, channel_messages
from auth import auth_logout

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channels_create(token, name, is_public) return { channel_id }
-> channel_join(token, channel_id) return {}
-> channel_messages(token, channel_id) return { messages }
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
    -> the authorised user is not a member of the channel that the
       message is within
Error type: InputError
    -> channel ID is not a valid channel
    -> message is more than 1000 characters
    -> an active standup is not currently running in this channel
'''

'''
assumptions
duration is a positive integer
each test is shorter than the duration
'''

def is_message_in_messages(str_message, messages):
    for message in messages:
        if str_message == message['message']:
            return True
    return False

def test_standup_send_basic(initialise_user_data, initialise_channel_data):
    token1 = initialise_user_data['admin']['token']
    token2 = initialise_user_data['user0']['token']
    channel1_id = initialise_channel_data['admin_publ']['channel_id']
    channel2_id = initialise_channel_data['user0_publ']['channel_id']
    duration = 1

    channel_join(token2, channel1_id)

    standup_start(token1, channel1_id, duration) #admin_publ
    standup_start(token2, channel2_id, duration) #user0_publ

    standup_send(token1, channel1_id, 'start of standup in admin_publ')
    standup_send(token2, channel1_id, 'end of standup in admin_publ')

    standup_send(token2, channel2_id, 'start of standup in user0_publ')

    #wait 1 seconds for standups to expire (and call standup_active() to update)
    time.sleep(2)
    standup_active(token1, channel1_id)
    standup_active(token1, channel2_id)

    with pytest.raises(InputError):
        standup_send(token1, channel1_id, 'standup has expired')

    admin_publ_standup_message = 'admin_first: start of standup in admin_publ\n' +\
                                 'user0_first: end of standup in admin_publ'
    user0_publ_standup_message = 'user0_first: start of standup in user0_publ'

    #get channel_messages
    admin_publ_messages = channel_messages(token1, channel1_id, 0)['messages']
    user0_publ_messages = channel_messages(token2, channel2_id, 0)['messages']

    assert is_message_in_messages(admin_publ_standup_message, admin_publ_messages)
    assert is_message_in_messages(user0_publ_standup_message, user0_publ_messages)


def test_standup_send_invalid_token(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)

    invalid_token = ' '

    with pytest.raises(AccessError):
        standup_send(invalid_token, channel_id, 'sent with invalid token')

def test_standup_send_not_in_channel(initialise_user_data, initialise_channel_data):
    standup_token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_priv']['channel_id']
    duration = 1

    standup_start(standup_token, channel_id, duration)

    message_token = initialise_user_data['user0']['token']

    with pytest.raises(AccessError):
        standup_send(message_token, channel_id, 'I am not in this channel')

def test_standup_send_invalid_channel(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)

    invalid_channel_id = -1

    with pytest.raises(InputError):
        standup_send(token, invalid_channel_id, 'sent with invalid channel_id')

def test_standup_send_long_short_message(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)

    with pytest.raises(InputError):
        standup_send(token, channel_id, 'aa'*1000)

    with pytest.raises(InputError):
        standup_send(token, channel_id, '')

def test_standup_send_not_active(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    with pytest.raises(InputError):
        standup_send(token, channel_id, 'there is no standup')

def test_standup_send_expire_leave(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)
    standup_send(token, channel_id, 'I am about to logout')

    auth_logout(token)

    #we still need a valid token
    user_token = initialise_user_data['user0']['token']
    channel_join(user_token, channel_id)

    #make sure message is still sent at end
    time.sleep(1)
    standup_active(user_token, channel_id)

    message = 'admin_first: I am about to logout'
    admin_publ_messages = channel_messages(user_token, channel_id, 0)['messages']

    assert is_message_in_messages(message, admin_publ_messages)

def test_standup_send_no_messages(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)

    time.sleep(1)
    standup_active(token, channel_id)

    #should send nothing
    messages = channel_messages(token, channel_id, 0)['messages']
    assert messages == []

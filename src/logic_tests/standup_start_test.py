'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

Iteration 3
'''

import time
import pytest
from error import AccessError, InputError
from standup import standup_start, standup_active, standup_send

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channels_create(token, name, is_public) return { channel_id }
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
Error type: InputError
    -> channel ID is not a valid channel
    -> an active standup is currently running in this channel
'''

'''
assumptions
duration is a positive integer
each test is shorter than the duration
'''

def test_standup_start_basic(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel1_id = initialise_channel_data['admin_publ']['channel_id']
    channel2_id = initialise_channel_data['admin_priv']['channel_id']

    standup_start(token, channel1_id, 1)
    standup_start(token, channel2_id, 3)

    time.sleep(2)
    standup_active(token, channel1_id)
    standup_active(token, channel2_id)

    with pytest.raises(InputError):
        standup_send(token, channel1_id, 'standup1 expired')

    standup_send(token, channel2_id, 'standup2 still valid')

    time.sleep(2)
    standup_active(token, channel1_id)
    standup_active(token, channel2_id)
    
    with pytest.raises(InputError):
        standup_send(token, channel2_id, 'standup2 expired')

def test_standup_start_invalid_token(initialise_channel_data):
    invalid_token = ' '
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    with pytest.raises(AccessError):
        standup_start(invalid_token, channel_id, duration)

def test_standup_start_invalid_channel(initialise_user_data):
    token = initialise_user_data['admin']['token']
    invalid_channel_id = -1
    duration = 1

    with pytest.raises(InputError):
        standup_start(token, invalid_channel_id, duration)

def test_standup_start_already_running(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    standup_start(token, channel_id, duration)

    with pytest.raises(InputError):
        standup_start(token, channel_id, duration)

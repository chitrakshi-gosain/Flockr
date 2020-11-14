'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

Iteration 3
'''

import time
import pytest
from error import AccessError, InputError
from standup import standup_start, standup_active

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
Error type: InputError
    -> channel ID is not a valid channel
'''

'''
assumptions
duration is a positive integer
each test is shorter than the duration
any user can call standup_active in any channel
'''

def test_standup_active_expiry(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    time_finish = standup_start(token, channel_id, 1)['time_finish']

    standup_info = standup_active(token, channel_id)
    assert standup_info['is_active']
    assert standup_info['time_finish'] == time_finish

    time.sleep(2)

    #now standup has expired
    standup_info = standup_active(token, channel_id)
    assert not standup_info['is_active']
    assert standup_info['time_finish'] == None

def test_standup_active_invalid_token(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    standup_start(token, channel_id, 1)

    invalid_token = ' '

    with pytest.raises(AccessError):
        assert standup_active(invalid_token, channel_id)

def test_standup_active_invalid_channel(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    standup_start(token, channel_id, 1)

    invalid_channel_id = -1

    with pytest.raises(InputError):
        assert standup_active(token, invalid_channel_id)

def test_standup_active_no_standup(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    standup_info = standup_active(token, channel_id)
    assert not standup_info['is_active']
    assert standup_info['time_finish'] == None

def test_standup_active_not_in_channel(initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    user_token = initialise_user_data['user0']['token'] # not in standup channel
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    time_finish = standup_start(token, channel_id, 1)['time_finish']

    standup_info = standup_active(user_token, channel_id)
    assert standup_info['is_active']
    assert standup_info['time_finish'] == time_finish

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor -

Iteration 1
'''

import pytest
from channel import channel_leave, channel_join, channel_details, channel_addowner
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channel_details(token, channel_id) return
   {name, owner_memers, all_members}
-> channels_create(token, name. is_public) return {channel_id}
-> channel_join(token, channel_id) return {}
-> channel_addowner(token, channel_id, u_id) return {}
-> channel_leave(token, channel_id) return {}

'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> Channel ID is not a valid channel
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2

def is_user_in_channel(user_id, token, channel_id):
    channel_members = channel_details(token, channel_id)['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def is_owner_in_channel(user_id, token, channel_id):
    owner_members = channel_details(token, channel_id)['owner_members']
    return len(list(filter(lambda user: user_id == user['u_id'], owner_members)))

def test_channel_leave_basic(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['admin']['token'], channel_id) #need valid token to call is_user_in channel
    channel_join(users['user0']['token'], channel_id)
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == True

    channel_leave(users['user0']['token'], channel_id)
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False


def test_channel_leave_invalid_channel(initialise_user_data):
    users = initialise_user_data

    invalid_channel_id = -1
    with pytest.raises(InputError):
        assert channel_leave(users['user0']['token'], invalid_channel_id)


def test_channel_leave_not_in_channel(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['admin']['token'], channel_id) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False
    with pytest.raises(AccessError): #expect AccessError as user is not in channel
        assert channel_leave(users['user0']['token'], channel_id)


def test_channel_join_invalid_token(initialise_channel_data):
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    invalid_token = ' '
    with pytest.raises(AccessError): #expect AccessError as token is invalid
        assert channel_leave(invalid_token, channel_id)


def test_channel_leave_owner(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['user0']['token'], channel_id)
    channel_addowner(users['admin']['token'], channel_id, users['user0']['u_id'])
    channel_leave(users['user0']['token'], channel_id)

    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False
    assert is_owner_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False

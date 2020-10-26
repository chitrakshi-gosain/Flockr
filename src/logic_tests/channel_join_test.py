'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 1
'''

import pytest
from channel import channel_join, channel_details
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
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS:
InputError when:
    -> Channel ID is not a valid channel
AccessError when:
    -> channel_id refers to a channel that is private (when the
        authorised user is not a global owner
'''

def is_user_in_channel(user_id, token, channel_id):
    channel_members = channel_details(token, channel_id)['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def test_channel_join_basic(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # make sure user0 is not in channel
    channel_join(users['admin']['token'], channel_id) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False
    # attempt to join
    channel_join(users['user0']['token'], channel_id)
    #now make sure user0 is in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == True


def test_channel_join_invalid_channel(initialise_user_data):
    users = initialise_user_data

    invalid_channel_id = -1
    with pytest.raises(InputError): #expect error as channel_id is invalid
        assert channel_join(users['user0']['token'], invalid_channel_id)


def test_channel_join_private_user(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id1 = initialise_channel_data['admin_publ']['channel_id']
    channel_id2 = initialise_channel_data['admin_priv']['channel_id']

    #make sure user0 us not in channel
    channel_join(users['admin']['token'], channel_id1) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'],channel_id2) == False
    with pytest.raises(AccessError): #expect error as channel is private and user0 is not an admin
        assert channel_join(users['user0']['token'], channel_id2)


def test_channel_join_private_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['user0_priv']['channel_id']

    #make sure admin is not in channel
    assert is_user_in_channel(users['admin']['u_id'], users['admin']['token'], channel_id) == False
    #attempt to join
    channel_join(users['admin']['token'], channel_id)
    #now admin should be in channel
    assert is_user_in_channel(users['admin']['u_id'], users['admin']['token'], channel_id) == True


def test_channel_join_invalid_token(initialise_channel_data):
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    invalid_token = ' '
    with pytest.raises(AccessError): #expect AccessError as token is invalid
        assert channel_join(invalid_token, channel_id)


def test_channel_join_already_member(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    # make sure user0 is not in channel
    channel_join(users['admin']['token'], channel_id) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == False
    # attempt to join
    channel_join(users['user0']['token'], channel_id)
    #now make sure user0 is in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == True
    #Try join a second time
    channel_join(users['user0']['token'], channel_id)
    #there should only ever one instance of user in each channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channel_id) == 1

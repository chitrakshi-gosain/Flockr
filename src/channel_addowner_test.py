# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channel_details(token, channel_id) return {name, owner_members, all_members}
-> channel_addowner(token, channel_id, u_id) return {}
-> channel_join(token, channel_id) return {}
-> channels_create(token, name, is_public) return {channel_id}
'''

'''
EXCEPTIONS
Error type: InputError
    -> channel_id is not a valid channel ID
    -> user with u_id is already an owner of the channel
Error type: AccessError
    -> token passed in is not a valid token
    -> authorised user is not an admin of the flockr or owner of the channel
'''

'''
KEEP IN MIND:
-> channels_create adds user (based on token) as member and owner of the channel
'''

import pytest
import auth
import helper
from channel import channel_addowner, channel_join
from channels import channels_create
from error import InputError, AccessError
from other import clear

# channel_addowner should add the user with the provided u_id
# to the list of owners of a channel with the provided channel_id
# assumes that u_id is already a member of the channel

# TESTS

def test_channel_addowner_noerrors():
    '''
    basic test with no edge case or errors raised
    '''
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    channel_join(token1, channel_id)

    assert not helper.is_channel_owner(u_id1, channel_id)
    # user0 adds user1 as owner
    channel_addowner(token0, channel_id, u_id1)
    assert helper.is_channel_owner(u_id1, channel_id)

def test_channel_addowner_invalidchannel():
    '''
    test that channel_addowner raises InputError
    if channel_id is not a valid channel_id
    '''
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    channel_join(token1, channel_id)

    # assume -1 is not a valid channel id
    channel_id = -1

    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_addowner(token0, channel_id, u_id1)

def test_channel_addowner_alreadyowner():
    '''
    test that channel_addowner raises InputError
    if user with provided u_id is already an owner of the channel
    '''
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    channel_join(token1, channel_id)

    # add user1 as owner
    channel_addowner(token0, channel_id, u_id1)
    assert helper.is_channel_owner(u_id1, channel_id)

    # attempt to add owner twice
    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_addowner(token0, channel_id, u_id1)

def test_channel_addowner_authnotowner():
    '''
    test that channel_addowner raises AccessError
    if the authorised user is not an owner of the channel
    '''
    clear()

    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']
    # user0 is admin of the flockr but not owner of the channel
    channel_join(token0, channel_id)

    # create second user
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # second user is not an owner of the channel
    channel_join(token1, channel_id)

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        channel_addowner(token1, channel_id, u_id1)

def test_channel_addowner_invalidtoken():
    '''
    test that channel_addowner raises AccessError
    if the provided token is not valid
    '''
    clear()

    user_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id, token = user_details['u_id'], user_details['token']

    channel_info = channels_create(token, "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(token, channel_id)

    # assume " " is always an invalid token
    token = " "

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        channel_addowner(token, channel_id, u_id)

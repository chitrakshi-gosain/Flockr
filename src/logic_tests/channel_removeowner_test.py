'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Joseph Knox

Iteration 1
'''

import pytest
import auth
from channel import channel_addowner, channel_removeowner, channel_join, channel_details
from channels import channels_create, channels_listall
from error import InputError, AccessError
from other import clear

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channel_details(token, channel_id) return {name, owner_members, all_members}
-> channel_addowner(token, channel_id, u_id) return {}
-> channel_removeowner(token, channel_id, u_id) return {}
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

# channel_removeowner should remove the user with the provided u_id
# from the list of owners of a channel with the provided channel_id
# assumes that u_id is already a member of the channel

@pytest.fixture
def reset():
    clear()

@pytest.fixture
def initialise_user_data(reset):
    # user0 is admin
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")

    return {
        'user0': user0_details,
        'user1': user1_details
    }

@pytest.fixture
def initialise_channel_data(initialise_user_data):
    # user0 creates channel, thus is owner and member
    # user1 joins channel, thus is member but not owner
    user0_details = initialise_user_data['user0']
    user1_details = initialise_user_data['user1']
    channel_id = channels_create(user0_details['token'], "ch_name0", True)['channel_id']
    channel_join(user1_details['token'], channel_id)

    return {
        'channel_id': channel_id
    }

# TESTS

# basic test with no edge case or errors raised
def test_channel_removeowner_noerrors(initialise_user_data, initialise_channel_data):

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = initialise_user_data['user0']
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = initialise_user_data['user1']
    u_id1 = user1_details['u_id']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['channel_id']

    # assert user with u_id1 is not an owner
    channel_dict = channel_details(token0, channel_id)
    assert not any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])

    # user0 adds user1 as owner
    channel_addowner(token0, channel_id, u_id1)

    # assert user with u_id1 is an owner
    channel_dict = channel_details(token0, channel_id)
    assert any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])
    
    # user0 removes user1 as owner
    channel_removeowner(token0, channel_id, u_id1)

    # assert user with u_id1 is not an owner
    channel_dict = channel_details(token0, channel_id)
    assert not any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])

# test that channel_removeowner raises InputError if channel_id is not a valid channel_id
def test_channel_removeowner_invalidchannel(initialise_user_data, initialise_channel_data):

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = initialise_user_data['user0']
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = initialise_user_data['user1']
    u_id1 = user1_details['u_id']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['channel_id']

    # user0 adds user1 as owner
    channel_addowner(token0, channel_id, u_id1)

    # assume -1 is not a valid channel id
    channel_id = -1

    # assert that channel_removeowner raises InputError
    with pytest.raises(InputError):
        channel_removeowner(token0, channel_id, u_id1)

# test that channel_removeowner raises InputError
# if user with provided u_id is not an owner of the channel
def test_channel_removeowner_notowner(initialise_user_data, initialise_channel_data):

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = initialise_user_data['user0']
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = initialise_user_data['user1']
    u_id1 = user1_details['u_id']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['channel_id']

    # assert user with u_id1 is not an owner
    channel_dict = channel_details(token0, channel_id)
    assert not any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])

    # user0 adds user1 as owner
    channel_addowner(token0, channel_id, u_id1)

    # assert user with u_id1 is an owner
    channel_dict = channel_details(token0, channel_id)
    assert any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])
    
    # user0 removes user1 as owner
    channel_removeowner(token0, channel_id, u_id1)

    # assert user with u_id1 is not an owner
    channel_dict = channel_details(token0, channel_id)
    assert not any(user['u_id'] == u_id1 for user in channel_dict['owner_members'])

    # attempt to remove owner twice
    # assert that channel_removeowner raises InputError
    with pytest.raises(InputError):
        channel_removeowner(token0, channel_id, u_id1)

# test that channel_removeowner raises AccessError
# if the authorised user is not an owner of the channel or admin of the flockr
def test_channel_removeowner_authnotowner(initialise_user_data, initialise_channel_data):

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = initialise_user_data['user0']
    u_id0 = user0_details['u_id']

    # user1 with u_id1 and token1 is not admin
    user1_details = initialise_user_data['user1']
    token1 = user1_details['token']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['channel_id']

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        channel_removeowner(token1, channel_id, u_id0)

# test that channel_removeowner raises AccessError
# if the authorised user is not an owner of the channel or the flockr
# i.e. test that channel_removeowner raises AccessError if token is invalid
def test_channel_removeowner_accesserror(initialise_user_data, initialise_channel_data):

    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['channel_id']

    # assume " " is always an invalid token
    token = " "

    # assert that channel_removeowner raises AccessError
    with pytest.raises(AccessError):
        channel_removeowner(token, channel_id, u_id)

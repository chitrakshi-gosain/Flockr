'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Joseph Knox

Iteration 1
'''

import pytest
import auth
from helper import is_channel_owner
from channel import channel_addowner, channel_removeowner, channel_join
from channels import channels_create
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

# TESTS

# basic test with no edge case or errors raised
def test_channel_removeowner_noerrors():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(user0['token'], channel_id)

    assert not is_channel_owner(user0['u_id'], channel_id)
    channel_addowner(admin['token'], channel_id, user0['u_id'])

    assert is_channel_owner(user0['u_id'], channel_id)
    channel_removeowner(admin['token'], channel_id, user0['u_id'])
    assert not is_channel_owner(user0['u_id'], channel_id)


# test that channel_removeowner raises InputError if channel_id is not a valid channel_id
def test_channel_removeowner_invalidchannel():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']

    channel_join(user0['token'], channel_id)

    channel_addowner(admin['token'], channel_id, user0['u_id'])

    # assume -1 is not a valid channel id
    invalid_channel_id = -1

    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_removeowner(admin['token'], invalid_channel_id, user0['u_id'])

# test that channel_removeowner raises InputError
# if user with provided u_id is not an owner of the channel
def test_channel_removeowner_notowner():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']

    channel_join(user0['token'], channel_id)

    # add owner
    channel_addowner(admin['token'], channel_id, user0['u_id'])
    assert is_channel_owner(user0['u_id'], channel_id)

    # attempt to remove owner twice
    channel_removeowner(admin['token'], channel_id, user0['u_id'])
    assert not is_channel_owner(user0['u_id'], channel_id)

    # assert that channel_removeowner raises InputError
    with pytest.raises(InputError):
        channel_removeowner(admin['token'], channel_id, user0['u_id'])

# test that channel_removeowner raises AccessError
# if the authorised user is not an owner of the channel or admin of the flockr
def test_channel_removeowner_authnotowner():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name0", True)
    channel_id = channel_info['channel_id']

    channel_join(user0['token'], channel_id)

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        channel_removeowner(user0['token'], channel_id, admin['u_id'])

# test that channel_removeowner raises AccessError
# if the authorised user is not an owner of the channel or the flockr
# i.e. test that channel_removeowner raises AccessError if token is invalid
def test_channel_removeowner_accesserror():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']

    # assume " " is always an invalid token
    invalid_token = " "

    # assert that channel_removeowner raises AccessError
    with pytest.raises(AccessError):
        channel_removeowner(invalid_token, channel_id, admin['u_id'])

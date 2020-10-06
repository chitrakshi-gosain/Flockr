from channel import channel_details, channel_addowner, channel_removeowner, channel_join
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear
import auth

# channel_removeowner should remove the user with the provided u_id to the list of owners of a channel with the provided channel_id
# assumes that u_id is already a member of the channel

# HELPER FUNCTIONS

# checks if user with u_id is an owner of channel with channel_id
def is_channel_owner(u_id, token, channel_id):
    channel_info = channel_details(token, channel_id)
    for owner in channel_info['owner_members']:
        if owner['u_id'] == u_id:
            return True
    return False

# TESTS

# basic test with no edge case or errors raised
def test_channel_removeowner_noerrors():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(user0['token'], channel_id)

    assert is_channel_owner(user0['u_id'], admin['token'], channel_id) == False
    channel_addowner(admin['token'], channel_id, user0['u_id'])

    assert is_channel_owner(user0['u_id'], admin['token'], channel_id) == True
    channel_removeowner(admin['token'], channel_id, user0['u_id'])
    assert is_channel_owner(user0['u_id'], admin['token'], channel_id) == False


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

# test that channel_removeowner raises InputError if user with provided u_id is not an owner of the channel
def test_channel_removeowner_notowner():
    clear()

    admin = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0 = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")

    channel_info = channels_create(admin['token'], "ch_name2", True)
    channel_id = channel_info['channel_id']

    channel_join(user0['token'], channel_id)

    # add owner
    channel_addowner(admin['token'], channel_id, user0['u_id'])
    assert is_channel_owner(user0['u_id'], admin['token'], channel_id) == True

    # attempt to remove owner twice
    channel_removeowner(admin['token'], channel_id, user0['u_id'])
    assert is_channel_owner(user0['u_id'], admin['token'], channel_id) == False

    # assert that channel_removeowner raises InputError
    with pytest.raises(InputError):
        channel_removeowner(admin['token'], channel_id, user0['u_id'])

# test that channel_removeowner raises AccessError if the authorised user is not an owner of the channel or admin of the flockr
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

# test that channel_removeowner raises AccessError if the authorised user is not an owner of the channel or the flockr
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

# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 1

from channel import channel_details, channel_addowner, channel_join
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear
import auth

# channel_addowner should add the user with the provided u_id to the list of owners of a channel with the provided channel_id
# assumes that u_id is already a member of the channel

### maybe also test for admin vs non-admin (global owners) (an admin is the first user to register in system)

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
def test_channel_addowner_noerrors():
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id0, token0 = user0_details['u_id'], user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    channel_join(token1, channel_id)

    assert not is_channel_owner(u_id1, token1, channel_id)
    # user0 adds user1 as owner
    channel_addowner(token0, channel_id, u_id1)
    assert is_channel_owner(u_id1, token1, channel_id)


# test that channel_addowner raises InputError if channel_id is not a valid channel_id
def test_channel_addowner_invalidchannel():
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id0, token0 = user0_details['u_id'], user0_details['token']

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


# test that channel_addowner raises InputError if user with provided u_id is already an owner of the channel
def test_channel_addowner_alreadyowner():
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id0, token0 = user0_details['u_id'], user0_details['token']

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
    assert is_channel_owner(u_id1, token0, channel_id)

    # attempt to add owner twice
    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_addowner(token0, channel_id, u_id1)


# test that channel_addowner raises AccessError if the authorised user is not an owner of the channel
def test_channel_addowner_authnotowner():
    clear()

    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id0, token0 = user0_details['u_id'], user0_details['token']

    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']
    # user0 is admin of the flockr but not owner of the channel
    channel_join(token0, channel_id)

    # create second user
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    token1 = user1_details['token']

    # second user is not an owner of the channel
    channel_join(token1, channel_id)

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        channel_addowner(token1, channel_id, u_id0)

# test that channel_addowner raises AccessError if the provided token is not valid
def test_channel_addowner_invalidtoken():
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

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
def channel_addowner_noerrors_test():
    clear()

    # user with u_id and token is the first to register, thus also admin of the flockr
    user_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id, token = user_details['u_id'], user_details['token']

    channel_info = channels_create(token, "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(token, channel_id)

    assert not is_channel_owner(u_id, token, channel_id)
    # user adds themselves as owner
    channel_addowner(token, channel_id, u_id)
    assert is_channel_owner(u_id, token, channel_id)


# test that channel_addowner raises InputError if channel_id is not a valid channel_id
def channel_addowner_invalidchannel_test():
    clear()

    user_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id, token = user_details['u_id'], user_details['token']

    channel_info = channels_create(token, "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(token, channel_id)

    # assume -1 is not a valid channel id
    channel_id = -1

    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_addowner(token, channel_id, u_id)


# test that channel_addowner raises InputError if user with provided u_id is already an owner of the channel
def channel_addowner_alreadyowner_test():
    clear()

    user_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    u_id, token = user_details['u_id'], user_details['token']

    channel_info = channels_create(token, "ch_name2", True)
    channel_id = channel_info['channel_id']
    channel_join(token, channel_id)

    # add owner
    channel_addowner(token, channel_id, u_id)
    assert is_channel_owner(u_id, token, channel_id)

    # attempt to add owner twice
    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        channel_addowner(token, channel_id, u_id)


# test that channel_addowner raises AccessError if the authorised user is not an owner of the channel
def channel_addowner_authnotowner_test():
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
def channel_addowner_invalidtoken_test():
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

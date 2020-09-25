from channel import channel_join, channel_details
from other import clear
import auth
import channels

import pytest
from error import InputError, AccessError

'''
Tests for channel_leave()

Parameters:(token, channel_id)

Return type: {}

Exceptions: InputError ->
                Channel ID is not a valid channel
            AccessError ->
                Authorised user is not a member of channel with channel_id

Description: Given a channel ID, the user removed as a member of this channel

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2

#note: these tests also require the functions to be implemented:
    #auth_register, channels_create, channel_details, channel_join, clear

'''
Current assumptions:
    1. Users are valid when/if they try leave the channel
    2. Should directly modify data if it works (and we check if data has changed to verify)
    3. Users cannot leave a channel if they are not in the channel

'''

'''
Test ideas: [description] - [pass / fail / error]
    1. channel_id is valid and user is in channel - pass
    2. Channel does not exist - InputError
    3. User is not part of the channel when they try leave - AccessError
'''

def initialise_data():
    # create users
    (admin_id, admin_token) = auth.auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    (user0_id, user0_token) = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    (user1_id, user1_token) = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")

    users_list = { 'admin' : [admin_id, admin_token],
                   'user0' : [user0_id, user0_token],
                   'user1' : [user1_id, user1_token] }
    # create channels
    channel_public_id = channels.channels_create(admin_token, "public0", True)
    channel_private_id = channels.channels_create(admin_token, "private0", False)

    channels_list = { 'public' : [channel_public_id], 'private' : channel_private_id }

    return (users_list, channels_list)

def user_in_channel(user_id, token, channel_id):
    (name, owners, members) = channel_details(token, channel_id)
    for member in members:
        if (member['u_id'] == user_id):
            return True
    return False


def test_channel_leave_basic():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    public, private = channels['public'], channels['private']

    channel_join(user0[1], public[0]) # user0_token, channel_id
    assert user_in_channel(user0[0], user0[1], public[0]) == True

    channel_leave(user0[1], public[0])
    assert user_in_channel(user0[0], user0[1], public[0]) == False
    clear()

def test_channel_leave_invalid_channel():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    public, private = channels['public'], channels['private']

    invalid_channel_id = (public[0] + private[0])/2 #should guarantee an invalid (different) id

    with pytest.raises(InputError) as e:
        assert channel_leave(user0[1], invalid_channel_id) #token, invalid_channel_id
    clear()

def test_channel_leave_not_in_channel():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    public, private = channels['public'], channels['private']

    assert user_in_channel(user0[0], user0[1], public[0]) == False
    with pytest.raises(AccessError) as e:
        assert channel_leave(user0[1], public)
    clear()

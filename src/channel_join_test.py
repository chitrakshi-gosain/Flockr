from channel import channel_invite, channel_join, channel_details
from other import clear
import auth
import channels

import pytest
from error import InputError, AccessError

'''
Tests for channel_join()

Interface:
Parameters:(token, channel_id)

Return type: {}

Exceptions: InputError ->
                Channel ID is not a valid channel
            AccessError ->
                channel_id refers to a channel that is private
                    (when the authorised user is not an admin)

Description: Given a channel_id of a channel that the authorised user can join,
             adds them to that channel

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2

#note: these tests also require the functions to be implemented:
    #auth_register, channels_create, channel_details, clear

'''
Current assumptions:
    1. User cannot join if they are already in the channel
    2. Users are valid when/if they try join the channel
    3. Should directly modify data if it works (and we check if data has changed to verify)

'''

'''
Test ideas: [description] - [pass / fail / error]
    1. valid public channel_id and user is not in channel - pass
    2. channel_id does not exist - InputError
    3. channel is private (and user is not admin) - AccessError
    4. channel is private (and user is admin) - pass
    5. user is already in channel - fail ----------------------- (How do we test this?)
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


def test_channel_join_basic():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['users0']
    public = channels['public']

    assert user_in_channel(user0[0], user0[1], public[0]) == False
    channel_join(user0[1], public[0]) #token, channel_id
    assert user_in_channel(user0[0], user0[1], public[0]) == True
    clear()

def test_channel_join_invalid_channel():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    public, private = channels['public'], channels['private']

    invalid_channel_id = (public[0] + private[0])/2 #should guarantee an invalid (different) id

    assert user_in_channel(user0[0], user0[1], public[0]) == False
    with pytest.raises(InputError) as e:
        assert channel_join(user0[1], invalid_channel_id) #token, invalid_channel_id
    clear()

def test_channel_join_private_user():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    private = channels['private']

    assert user_in_channel(user0[1], private[0]) == False
    with pytest.raises(AccessError) as e:
        assert channel_join(user0[1], private[0]) #token, invalid_channel_id
    clear()

def test_channel_join_private_admin():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    private = channels['private']

    #how to properly set admin?
    assert user_in_channel(admin[1], private) == False
    channel_join(admin[1], private[0]) #token, channel_id
    assert user_in_channel(admin[1], private) == True
    clear()

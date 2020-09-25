from channel import channel_invite, channel_join, channel_details
from other import clear
import auth
import channels

import pytest
from error import InputError, AccessError

'''
Tests for channel_invite()

Parameters:(token, channel_id, u_id)

Return type: {}

Exceptions: InputError ->
                channel_id does not reffer to a valid channel that the
                    authorised user is part of
                u_id does not refer to valid user
            AccessError ->
                the authorised user is not already a member of the channel

Description: Invites a user (with user id u_id) to join a channel with ID
             channel_id. Once invited the user is added to the channel
             immediately

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2

#note: these tests also require the functions to be implemented:
    #auth_register, channels_create, channel_details, channel_join, clear


'''
Current assumptions:
    1. User cannot be invited if they are already in the channel
'''

'''
Test ideas: [description] - [pass / fail / error]
    1. valid channel_id and users - pass
    2. channel_id is invalid - InputError
    3. invalid user is added - InputError
    4. authorised user is not in channel - AccessError
    5. user is already in channel - fail -----------------(How do we test?)
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


def test_channel_invite_valid_basic():
    (users, channels) = initialise_data()
    admin, users0 = users["admin"], users['users0']
    public = channels['public']

    channel_join(admin[1], public[0]) # token, channel_id

    assert user_in_channel(user0[0], admin[1], public[0]) == False
    channel_invite(admin[1], public[0], user0[0]) # admin_token, channel_id, user_id
    assert user_in_channel(user0[0], admin[1], public[0]) == True
    clear()

def test_channel_invite_invalid_channel():
    (users, channels) = initialise_data()
    admin, user0 = users["admin"], users['user0']
    public, private = channels['public'], channels['private']

    channel_join(admin[1], public[0]) # token, channel_id

    invalid_channel_id = (public[0] + private[0])/2 #should guarantee an invalid (different) id
    with pytest.raises(InputError) as e:
        assert channel_invite(admin[1], invalid_channel_id, user0[0]) # admin_token, invalid_id, user_id
    clear()

def test_channel_invite_invalid_user():
    (users, channels) = initialise_data()
    admin, user0, user1 = users["admin"], users['user0'], users['user1']
    public = channels['public']

    channel_join(admin[1], public[0]) # token, channel_id

    invalid_user_id = admin[0] + user0[0] + user1[0] #should garantee an invalid id
    with pytest.raises(InputError) as e:
        assert channel_invite(admin[1], public[0], invalid_user_id) # admin_token, channel_id, invalid_user_id
    clear()

def test_channel_invite_invoker_not_in_channel():
    (users, channels) = initialise_data()
    admin, user0, user1 = users["admin"], users['user0'], users['user1']
    public = channels['public']

    assert user_in_channel(user0[0], admin[1], public[0]) == False
    with pytest.raises(AccessError) as e:
        assert channel_invite(user1[1], public[0], invalid_user_id) # user1_token, channel_id, user_id
    #Should be AccessError as user1 was not in channel
    clear()

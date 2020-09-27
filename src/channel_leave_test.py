from channel import channel_leave, channel_join, channel_details
from other import clear
from auth import auth_register
from channels import channels_create

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
    1. " " is an invalid token
    2. ids can only be non-negative integers
'''

'''
Test ideas: [description] - [pass / fail / error]
    1. channel_id is valid and user is in channel - pass
    2. Channel does not exist - InputError
    3. User is not part of the channel when they try leave - AccessError
    4. user has invalid token - AccessError
'''

def initialise_data():
    #create users
    #The first user to sign up is global owner
    (admin_id, admin_token) = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    (user0_id, user0_token) = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    (user1_id, user1_token) = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    #create channels
    channel_publ_id = channels_create(admin_token, "publ0", True)
    channel_priv_id = channels_create(admin_token, "priv0", False)

    return { # users
        'admin' : {'u_id': admin_id, 'token': admin_token, 'is_admin': True},
        'user0' : {'u_id': user0_id, 'token': user0_token, 'is_admin': False},
        'user1' : {'u_id': user1_id, 'token': user1_token, 'is_admin': False},
    },
    { # channels
        'publ' : {'ch_id': channel_publ_id},
        'priv' : {'ch_id': channel_priv_id},
    }

def is_user_in_channel(user_id, token, channel_id):
    (name, owners, members) = channel_details(token, channel_id)
    for member in members:
        if (member['u_id'] == user_id):
            return True
    return False


def test_channel_leave_basic():
    clear()
    users, channels = initialise_data()

    channel_join(users['user0']['token'], channels['publ']['ch_id'])
    assert is_user_in_channel(users['user0']['u_id'], users['user0']['token'], channels['publ']['u_id']) == True

    channel_leave(users['user0']['token'], channels['publ']['ch_id'])
    assert is_user_in_channel(users['user0']['u_id'], users['user0']['token'], channels['publ']['u_id']) == False


def test_channel_leave_invalid_channel():
    clear()
    users, channels = initialise_data()

    invalid_channel_id = -1
    with pytest.raises(InputError) as e:
        assert channel_leave(users['user0']['token'], invalid_channel_id)


def test_channel_leave_not_in_channel():
    clear()
    users, channels = initialise_data()

    assert is_user_in_channel(users['user0']['u_id'], users['user0']['token'], channels['publ']['u_id']) == False
    with pytest.raises(AccessError) as e: #expect AccessError as user is not in channel
        assert channel_leave(users['user0']['token'], channels['publ']['ch_id'])


def test_channel_join_invalid_token():
    clear()
    users, channels = initialise_data()

    invalid_token = ' '
    with pytest.raises(AccessError) as e: #expect AccessError as token is invalid
        assert channel_leave(invalid_token, channels['publ']['ch_id'])

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
    admin_details = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0_details = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    user1_details = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    #create channels
    channel_publ_details = channels_create(admin_details['token'], "publ0", True)
    channel_priv_details = channels_create(admin_details['token'], "priv0", False)

    return ({ # users
        'admin' : admin_details,
        'user0' : user0_details,
        'user1' : user1_details,
    },
    { # channels
        'publ' : channel_publ_details,
        'priv' : channel_priv_details,
    })

def is_user_in_channel(user_id, token, channel_id):
    channel_info = channel_details(token, channel_id)
    for member in channel_info['all_members']:
        if (member['u_id'] == user_id):
            return True
    return False


def test_channel_leave_basic():
    clear()
    users, channels = initialise_data()

    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == True

    channel_leave(users['user0']['token'], channels['publ']['channel_id'])
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False


def test_channel_leave_invalid_channel():
    clear()
    users = initialise_data()[0]

    invalid_channel_id = -1
    with pytest.raises(InputError):
        assert channel_leave(users['user0']['token'], invalid_channel_id)


def test_channel_leave_not_in_channel():
    clear()
    users, channels = initialise_data()

    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False
    with pytest.raises(AccessError): #expect AccessError as user is not in channel
        assert channel_leave(users['user0']['token'], channels['publ']['channel_id'])


def test_channel_join_invalid_token():
    clear()
    channels = initialise_data()[1]

    invalid_token = ' '
    with pytest.raises(AccessError): #expect AccessError as token is invalid
        assert channel_leave(invalid_token, channels['publ']['channel_id'])

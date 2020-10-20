'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - 

Iteration 1
'''

import pytest
from channel import channel_leave, channel_join, channel_details, channel_addowner
from other import clear
from auth import auth_register
from channels import channels_create
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> intialise_user_data() return { users }, { channels }
-> is_user_in_channel(user_id, token, channel_id) return amount of times u_id was found in channel
-> is_owner_in_channel(user_id, token, channel_id) return amount of times u_id was found in owner_members
-> test_channel_leave_basic()
-> test_channel_leave_invalid_channel()
-> test_channel_leave_not_in_channel()
-> test_channel_leave_invalid_token()
-> test_channel_leave_owner()
'''

'''
----channel_leave Documentation----

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
    channel_members = channel_details(token, channel_id)['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def is_owner_in_channel(user_id, token, channel_id):
    owner_members = channel_details(token, channel_id)['owner_members']
    return len(list(filter(lambda user: user_id == user['u_id'], owner_members)))

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


def test_channel_leave_owner():
    clear()
    users, channels = initialise_data()

    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    channel_addowner(users['admin']['token'], channels['publ']['channel_id'], users['user0']['u_id'])
    channel_leave(users['user0']['token'], channels['publ']['channel_id'])

    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False
    assert is_owner_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False

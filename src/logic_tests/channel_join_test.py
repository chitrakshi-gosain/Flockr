'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - 

Iteration 1
'''

import pytest
from channel import channel_join, channel_details
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
-> test_channel_join_basic()
-> test_channel_join_invalid_channel()
-> test_channel_join_private_user()
-> test_channel_join_private_admin()
-> test_channel_join_invalid_token()
-> test_channel_join_already_member()
'''

'''
----channel_join Documentation----
Parameters:
(token, channel_id)

Return Type:
{}

Exceptions:
    InputError when:
        -> Channel ID is not a valid channel
    AccessError when:
        -> channel_id refers to a channel that is private (when the authorised user is not a global owner)

Description: Given a channel_id of a channel that the
             authorised user can join, adds them to that channel
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

    channel_priv_user_details = channels_create(user0_details['token'], 'priv1', False)

    return ({ # users
        'admin' : admin_details,
        'user0' : user0_details,
        'user1' : user1_details,
    },
    { # channels
        'publ' : channel_publ_details,
        'priv' : channel_priv_details,
        'user_priv' : channel_priv_user_details,
    })

def is_user_in_channel(user_id, token, channel_id):
    channel_members = channel_details(token, channel_id)['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def test_channel_join_basic():
    clear()
    users, channels = initialise_data()
    # make sure user0 is not in channel
    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False
    # attempt to join
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #now make sure user0 is in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == True


def test_channel_join_invalid_channel():
    clear()
    users = initialise_data()[0]

    invalid_channel_id = -1
    with pytest.raises(InputError): #expect error as channel_id is invalid
        assert channel_join(users['user0']['token'], invalid_channel_id)


def test_channel_join_private_user():
    clear()
    users, channels = initialise_data()
    #make sure user0 us not in channel
    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'],channels['priv']['channel_id']) == False
    with pytest.raises(AccessError): #expect error as channel is private and user0 is not an admin
        assert channel_join(users['user0']['token'], channels['priv']['channel_id'])


def test_channel_join_private_admin():
    clear()
    users, channels = initialise_data()

    #make sure admin is not in channel
    assert is_user_in_channel(users['admin']['u_id'], users['admin']['token'], channels['user_priv']['channel_id']) == False
    #attempt to join
    channel_join(users['admin']['token'], channels['user_priv']['channel_id'])
    #now admin should be in channel
    assert is_user_in_channel(users['admin']['u_id'], users['admin']['token'], channels['user_priv']['channel_id']) == True


def test_channel_join_invalid_token():
    clear()
    channels = initialise_data()[1]

    invalid_token = ' '
    with pytest.raises(AccessError): #expect AccessError as token is invalid
        assert channel_join(invalid_token, channels['publ']['channel_id'])


def test_channel_join_already_member():
    clear()
    users, channels = initialise_data()

    # make sure user0 is not in channel
    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == False
    # attempt to join
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #now make sure user0 is in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == True
    #Try join a second time
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #there should only ever one instance of user in each channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id']) == 1

'''
Created collaboratively by Wed15Team2 2020 T3
Contributer - Jordan Hunyh

Iteration 1
'''

import pytest
from channel import channel_invite, channel_join, channel_details
from other import clear
from auth import auth_register
from channels import channels_create
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> channels_create(token) return {channel_id}
-> channel_join(token, channel_id) return {}
-> channel_invite(token, channel_id, u_id) return {}
-> channel_details(token, channel_id) return
   {name, owner_members, all_members}
'''

'''
EXCEPTIONS
Error type: InputError
    -> channel_id does not refer to a valid channel
    -> u_id does not refer to a valid user
Error type: AccessError
    -> the authorised user is not already a member of the channel
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

    channel_priv_user_details = channels_create(user0_details['token'], 'priv1', False)

    return ({ # users
        'admin' : admin_details,
        'user0' : user0_details,
        'user1' : user1_details,
    },
    { # channels
        'publ' : channel_publ_details,
        'priv' : channel_priv_details,
        'user_priv' : channel_priv_user_details
    })


def is_user_in_channel(user_id, token, channel_id):
    channel_members = channel_details(token, channel_id)['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def test_channel_invite_valid_basic():
    clear()
    users, channels = initialise_data()
    #add user0 to public channel so they can invite
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #make sure user1 is not in channel
    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token to call is_user_in channel
    assert not is_user_in_channel(users['user1']['u_id'], users['admin']['token'], channels['publ']['channel_id'])

    #have user0 invite user1 to public channel
    channel_invite(users['user0']['token'], channels['publ']['channel_id'], users['user1']['u_id'])
    #now make sure user1 is in public channel
    assert is_user_in_channel(users['user1']['u_id'], users['user0']['token'], channels['publ']['channel_id'])


def test_channel_invite_invalid_channel():
    clear()
    users = initialise_data()[0]

    invalid_channel_id = -1
    with pytest.raises(InputError): #expect InputError as channel is invalid
        assert channel_invite(users['admin']['token'], invalid_channel_id, users['user0']['u_id'])


def test_channel_invite_invalid_user():
    clear()
    users, channels = initialise_data()

    channel_join(users['admin']['token'], channels['publ']['channel_id'])

    invalid_user_id = -1
    with pytest.raises(InputError): # expect InputError as u_id is invalid
        assert channel_invite(users['admin']['token'], channels['publ']['channel_id'], invalid_user_id)


def test_channel_invite_invoker_not_in_channel():
    clear()
    users, channels = initialise_data()
    #make sure invoker (user0) is not in channel
    channel_join(users['admin']['token'], channels['publ']['channel_id']) #need valid token in channel (admin)
    assert not is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['channel_id'])
    with pytest.raises(AccessError): #expect AccessError as invoker was not in channel
        assert channel_invite(users['user0']['token'], channels['publ']['channel_id'], users['user1']['u_id'])

def test_channel_invite_invalid_token():
    clear()
    users, channels = initialise_data()

    invalid_token = ' '
    with pytest.raises(AccessError): #expect AccessError as token is invalid
        assert channel_invite(invalid_token, channels['publ']['channel_id'], users['user1']['u_id'])


def test_channel_invite_already_in_channel():
    clear()
    users, channels = initialise_data()
    #add user0 to public channel so they can invite
    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #make sure user1 is not in channel
    assert not is_user_in_channel(users['user1']['u_id'], users['admin']['token'], channels['publ']['channel_id'])

    #have user0 invite user1 to public channel
    channel_invite(users['user0']['token'], channels['publ']['channel_id'], users['user1']['u_id'])
    #now make sure user1 is in public channel
    assert is_user_in_channel(users['user1']['u_id'], users['user0']['token'], channels['publ']['channel_id'])
    #now try invite for a second time
    channel_invite(users['user0']['token'], channels['publ']['channel_id'], users['user1']['u_id'])
    #there should only ever one instance of user in each channel
    assert is_user_in_channel(users['user1']['u_id'], users['user0']['token'], channels['publ']['channel_id']) == 1

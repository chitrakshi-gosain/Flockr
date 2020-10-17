from channel import channel_join, channel_leave
from other import clear, admin_userpermission_change
from auth import auth_register
from channels import channels_create

import pytest
from error import InputError, AccessError

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> intialise_data() return { users }, { channels }
-> test_other_admin_userpermission_change_make_admin()
-> test_other_admin_userpermission_change_remove_admin()
-> test_other_admin_userpermission_change_remove_self()
-> test_other_admin_userpermission_change_remove_last()
-> test_other_admin_userpermission_change_invalid_permission_id()
-> test_other_admin_userpermission_change_invalid_uid()
-> test_other_admin_userpermission_change_invalid_token()
'''

'''
----admin_userpermission_change Documentation----

HTTP Method: POST

Parameters:(token, u_id, permission_id)

Return type: {}

Exceptions: InputError ->
                u_id does not refer to a valid user
                permission_id does not refer to a value permission
            AccessError ->
                The authorised user is not an owner

Description: Given a User by their user ID, set their permissions to
             new permissions described by permission_id

'''

'''
Assumptions:
1. There must always be at least 1 global owner
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
        'user_priv' : channel_priv_user_details,
    })

def test_other_admin_userpermission_change_make_admin():
    clear()
    users, channels = initialise_data()

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channels['priv']['channel_id'])

    #make them admin
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)

    #Now try get them to join channel
    channel_join(users['user0']['token'], channels['priv']['channel_id']) #throws no errors

def test_other_admin_userpermission_change_remove_admin():
    clear()
    users, channels = initialise_data()

    #make user0 owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)
    #try join private channel
    channel_join(users['user0']['token'], channels['priv']['channel_id']) #throws no errors

    channel_leave(users['user0']['token'], channels['priv']['channel_id'])

    #make them non-owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 2)

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channels['priv']['channel_id'])

def test_other_admin_userpermission_change_remove_self():
    clear()
    users, channels = initialise_data()

    #make user0 owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)
    #remove themselves as owner
    admin_userpermission_change(users['user0']['token'], users['user0']['u_id'], 2)

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channels['priv']['channel_id'])

def test_other_admin_userpermission_change_remove_last():
    clear()
    users, channels = initialise_data()

    #Try remove themselves as admin - but unable as they are the only admin
    admin_userpermission_change(users['admin']['token'], users['admin']['u_id'], 2)
    #They can still join a prviate channel as they are the only admin
    channel_join(users['admin']['token'], channels['user_priv']['channel_id'])

def test_other_admin_userpermission_change_non_admin():
    clear()
    users = initialise_data()[0]

    with pytest.raises(AccessError):
        admin_userpermission_change(users['user0']['token'], users['user0']['u_id'], 1)

def test_other_admin_userpermission_change_invalid_permission_id():
    clear()
    users = initialise_data()[0]

    invalid_permission_id = -1

    with pytest.raises(InputError):
        admin_userpermission_change(users['admin']['token'], users['user0']['u_id'],invalid_permission_id)

def test_other_admin_userpermission_change_invalid_uid():
    clear()
    users = initialise_data()[0]

    invalid_user_id = -1

    with pytest.raises(InputError):
        admin_userpermission_change(users['admin']['token'], invalid_user_id, 1)

def test_other_admin_userpermission_change_invalid_token():
    clear()
    users = initialise_data()[0]

    invalid_token = ' '

    with pytest.raises(AccessError):
        admin_userpermission_change(invalid_token, users['user0']['u_id'], 1)

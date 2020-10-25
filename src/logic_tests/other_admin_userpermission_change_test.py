'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
'''

import pytest
from channel import channel_join, channel_leave
from other import clear, admin_userpermission_change
from auth import auth_register
from channels import channels_create
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

def test_other_admin_userpermission_change_make_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_priv']['channel_id']

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channel_id)

    #make them admin
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)

    #Now try get them to join channel
    channel_join(users['user0']['token'], channel_id) #throws no errors

def test_other_admin_userpermission_change_remove_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_priv']['channel_id']

    #make user0 owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)
    #try join private channel
    channel_join(users['user0']['token'], channel_id) #throws no errors

    channel_leave(users['user0']['token'], channel_id)

    #make them non-owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 2)

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channel_id)

def test_other_admin_userpermission_change_remove_self(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_priv']['channel_id']

    #make user0 owner
    admin_userpermission_change(users['admin']['token'], users['user0']['u_id'], 1)
    #remove themselves as owner
    admin_userpermission_change(users['user0']['token'], users['user0']['u_id'], 2)

    #Try get user0 to join private channel
    with pytest.raises(AccessError):
        assert channel_join(users['user0']['token'], channel_id)

def test_other_admin_userpermission_change_remove_last(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['user1_priv']['channel_id']

    #Try remove themselves as admin - but unable as they are the only admin
    admin_userpermission_change(users['admin']['token'], users['admin']['u_id'], 2)
    #They can still join a prviate channel as they are the only admin
    channel_join(users['admin']['token'], channel_id)

def test_other_admin_userpermission_change_non_admin(initialise_user_data):
    users = initialise_user_data

    with pytest.raises(AccessError):
        admin_userpermission_change(users['user0']['token'], users['user0']['u_id'], 1)

def test_other_admin_userpermission_change_invalid_permission_id(initialise_user_data, initialise_channel_data):
    users = initialise_user_data

    invalid_permission_id = -1

    with pytest.raises(InputError):
        admin_userpermission_change(users['admin']['token'], users['user0']['u_id'],invalid_permission_id)

def test_other_admin_userpermission_change_invalid_uid(initialise_user_data, initialise_channel_data):
    users = initialise_user_data

    invalid_user_id = -1

    with pytest.raises(InputError):
        admin_userpermission_change(users['admin']['token'], invalid_user_id, 1)

def test_other_admin_userpermission_change_invalid_token(initialise_user_data, initialise_channel_data):
    users = initialise_user_data

    invalid_token = ' '

    with pytest.raises(AccessError):
        admin_userpermission_change(invalid_token, users['user0']['u_id'], 1)

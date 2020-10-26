'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
'''

import pytest
from channel import channel_join, channel_leave
from other import admin_userpermission_change
from error import InputError, AccessError

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> channel_join(token, channel_id) return {}
-> channel_leave(token, channel_id) return {}
-> admin_userpermission_change(token, u_id, permission_id) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user is not an owner
Error type: InputError
-> u_id does not refer to a valid user
-> permission_id does not refer to a value permission
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
    channel_id = initialise_channel_data['user0_priv']['channel_id']

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

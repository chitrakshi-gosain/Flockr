from channel import channel_invite, channel_join, channel_details
from other import clear
from auth import auth_register
from channels import channels_create

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

def create_user_data():
    (admin_id, admin_token) = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    (user0_id, user0_token) = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    (user1_id, user1_token) = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")

    return {
        'admin' : {'u_id': admin_id, 'token': admin_token},
        'user0' : {'u_id': user0_id, 'token': user0_token},
        'user1' : {'u_id': user1_id, 'token': user1_token},
    }

def create_channel_data():
    channel_publ_id = channels_create(admin_token, "public0", True)
    channel_priv_id = channels_create(admin_token, "private0", False)

    return {
        'publ' : {'ch_id': channel_publ_id},
        'priv' : {'ch_id': channel_priv_id},
    }

def is_user_in_channel(user_id, token, channel_id):
    (name, owners, members) = channel_details(token, channel_id)
    for member in members:
        if (member['u_id'] == user_id):
            return True
    return False


def test_channel_invite_valid_basic():
    clear()
    users, channels = create_user_data(), create_channel_data()
    #add admin to public channel so they can invite
    channel_join(users['admin']['token'], channels['publ']['ch_id']) # token, channel_id
    #make sure user0 is not in channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['ch_id']) == False

    #have admin invite user0 to public channel
    channel_invite(users['admin']['token'], channels['publ']['ch_id'], users['user0']['u_id'])
    #now make sure user0 is in public channel
    assert is_user_in_channel(users['user0']['u_id'], users['admin']['token'], channels['publ']['ch_id']) == True


def test_channel_invite_invalid_channel():
    clear()
    users, channels = create_user_data(), create_channel_data()

    channel_join(users['admin']['token'], channels['publ']['ch_id'])
    #create an invalid ch_id by averaging the two existing channle_ids
    invalid_channel_id = (channels['publ']['ch_id'] + channels['priv']['ch_id'])/2
    with pytest.raises(InputError) as e: #expect InputError as channel is invalid
        assert channel_invite(users['admin']['token'], invalid_channel_id, users['user0']['u_id'])


def test_channel_invite_invalid_user():
    clear()
    users, channels = create_user_data(), create_channel_data()

    channel_join(users['admin']['token'], channels['publ']['ch_id']) # token, channel_id
    #create an invalid u_id by summing the three existing u_ids
    invalid_user_id = users['admin']['u_id'] + users['admin']['u_id'] + users['admin']['u_id']
    with pytest.raises(InputError) as e: # expect InputError as u_id is invalid
        assert channel_invite(users['admin']['token'], channels['publ']['ch_id'], invalid_user_id)


def test_channel_invite_invoker_not_in_channel():
    clear()
    users, channels = create_user_data(), create_channel_data()
    #make sure invoker (user0) is not in channel
    assert is_user_in_channel(users['user0']['u_id'], users['user0']['token'], channels['publ']['ch_id']) == False
    with pytest.raises(AccessError) as e: #expect AccessError as invoker was not in channel
        assert channel_invite(users['user0']['token'], channels['publ']['ch_id'], users['user1']['u_id'])

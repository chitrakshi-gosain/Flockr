'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

Iteration 2
'''

import json
import requests
import pytest

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
    -> token is invalid
'''



# Jordan Huynh (z5169771)
# Wed15 Grape 2
def is_user_in_channel(url, user_id, token, channel_id):
    datain = {"token": token, "channel_id": channel_id}
    channel_members = requests.get(url+ "channel/details", params=datain).json()['all_members']

    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))


def test_invite_basic(url, initialise_user_data, initialise_channel_data):
    '''
    basic test with no edge cases or errors raised
    '''
    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    assert is_user_in_channel(url, u_id, token, channel_id) == 0

    invite_input = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    response = requests.post(url + "/channel/invite", json=invite_input)

    assert is_user_in_channel(url, u_id, token, channel_id) == 1

    assert response.status_code == 200

def test_invite_invalid_channel(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_invite raises InputError
    if channel_id does not refer to a valid channel
    '''
    invite_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": -1,
        "u_id": initialise_user_data['user1']['u_id']
    }
    response = requests.post(url + "/channel/invite", json=invite_input)

    assert response.status_code == 400

def test_invite_invalid_user(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_invite raises InputError
    if u_id does not refer to a valid user
    '''
    invite_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "u_id": -1
    }
    response = requests.post(url + "/channel/invite", json=invite_input)

    assert response.status_code == 400

def test_invite_invoker_not_in_channel(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_invite raises AccessError
    if the authorised user is not already a member of the channel
    '''
    token = initialise_user_data['user2']['token']
    u_id = initialise_user_data['admin']['u_id']
    channel_id = initialise_channel_data['user1_priv']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    invite_input = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    response = requests.post(url + "/channel/invite", json=invite_input)

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0
    assert response.status_code == 400

def test_invite_invalid_token(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_invite raises AccessError
    if token is invalid
    '''
    invite_input = {
        "token": ' ',
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "u_id": initialise_user_data['user1']['u_id']
    }
    response = requests.post(url + "/channel/invite", json=invite_input)

    assert response.status_code == 400

def test_channel_invite_already_in_channel(url, initialise_user_data, initialise_channel_data):
    '''
    check that a user can be invited to a channel they are already in
    '''
    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    assert is_user_in_channel(url, u_id, token, channel_id) == 0

    invite_input = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    }
    response = requests.post(url + "/channel/invite", json=invite_input)
    assert is_user_in_channel(url, u_id, token, channel_id) == 1
    assert response.status_code == 200

    #invite again
    response = requests.post(url + "/channel/invite", json=invite_input)
    assert is_user_in_channel(url, u_id, token, channel_id) == 1
    assert response.status_code == 200

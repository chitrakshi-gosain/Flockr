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
'''



# Jordan Huynh (z5169771)
# Wed15 Grape 2
def is_user_in_channel(url, user_id, token, channel_id):
    datain = {"token": token, "channel_id": channel_id}
    channel_members = requests.get(url+ "channel/details", params=datain).json()['all_members']
    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))

def is_owner_in_channel(url, user_id, token, channel_id):
    datain = {"token": token, "channel_id": channel_id}
    owner_members = requests.get(url+ "channel/details", params=datain).json()['owner_members']
    return len(list(filter(lambda user: user_id == user['u_id'], owner_members)))


def test_leave_basic(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    leave_input = {
        "token": token,
        "channel_id": channel_id,
    }
    #join channel
    requests.post(url + "/channel/join", json=leave_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1

    #attempt to leave
    response = requests.post(url + "/channel/leave", json=leave_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0
    assert response.status_code == 200

def test_leave_invalid_channel(url, initialise_user_data, initialise_channel_data):

    leave_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": -1,
    }
    response = requests.post(url + "/channel/leave", json=leave_input)

    assert response.status_code == 400

def test_leave_not_in_channel(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    #make sure user0 is not in channel
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    leave_input = {
        "token": token,
        "channel_id": channel_id,
    }
    response = requests.post(url + "/channel/leave", json=leave_input)

    assert response.status_code == 400

def test_leave_invalid_token(url, initialise_user_data, initialise_channel_data):

    leave_input = {
        "token": ' ',
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
    }
    response = requests.post(url + "/channel/leave", json=leave_input)

    assert response.status_code == 400

def test_leave_owner(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    leave_input = {
        "token": token,
        "channel_id": channel_id,
    }

    #join channel
    requests.post(url + "/channel/join", json=leave_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1

    #make user0 owner
    requests.post(url +"/channel/addowner", json={
        "token": admin_token,
        "channel_id": channel_id,
        "u_id": u_id
    })
    assert is_owner_in_channel(url, u_id, admin_token, channel_id) == 1

    #attempt to leave
    response = requests.post(url + "/channel/leave", json=leave_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0
    assert is_owner_in_channel(url, u_id, admin_token, channel_id) == 0
    assert response.status_code == 200

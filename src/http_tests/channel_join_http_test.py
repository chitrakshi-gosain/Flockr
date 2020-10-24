'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor -

Iteration 1
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> is_user_in_channel(url, user_id, token, channel_id) return amount of times u_id was found in channel
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
    InputError (400) when:
        -> Channel ID is not a valid channel
    AccessError (400) when:
        -> channel_id refers to a channel that is private (when the authorised user is not a global owner)

Description: Given a channel_id of a channel that the
             authorised user can join, adds them to that channel
'''



# Jordan Huynh (z5169771)
# Wed15 Grape 2
def is_user_in_channel(url, user_id, token, channel_id):
    datain = {"token": token, "channel_id": channel_id}
    channel_members = requests.get(url+ "channel/details", params=datain).json()['all_members']

    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))


def test_join_basic(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    join_input = {
        "token": token,
        "channel_id": channel_id
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1

    assert response.status_code == 200

def test_join_invalid_channel(url, initialise_user_data, initialise_channel_data):

    join_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": -1
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert response.status_code == 400

def test_join_private_user(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_priv']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    join_input = {
        "token": token,
        "channel_id": channel_id
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0
    assert response.status_code == 400

def test_join_private_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['admin']['u_id']
    channel_id = initialise_channel_data['user1_priv']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    join_input = {
        "token": token,
        "channel_id": channel_id
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1
    assert response.status_code == 200

def test_join_invalid_token(url, initialise_user_data, initialise_channel_data):

    join_input = {
        "token": " ",
        "channel_id": initialise_channel_data['admin_publ']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert response.status_code == 400

def test_join_already_member(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    admin_token = initialise_user_data['admin']['token']

    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 0

    join_input = {
        "token": token,
        "channel_id": channel_id
    }
    response = requests.post(url + "/channel/join", json=join_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1
    assert response.status_code == 200

    #join again
    response = requests.post(url + "/channel/join", json=join_input)
    assert is_user_in_channel(url, u_id, admin_token, channel_id) == 1
    assert response.status_code == 200

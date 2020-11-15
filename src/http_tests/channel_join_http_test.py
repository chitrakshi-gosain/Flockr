'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
'''

import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
-> APP.route("/channel/join", methods=['POST']) return
    json.dumps({})
-> APP.route("/channel/details", methods=['GET']) return
    json.dumps({name, owner_members, all_members})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
Exceptions:
    InputError (400) when:
        -> Channel ID is not a valid channel
    AccessError (400) when:
        -> channel_id refers to a channel that is private (when the authorised user is not a global owner)
        -> token is invalid

Description: Given a channel_id of a channel that the
             authorised user can join, adds them to that channel
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def is_user_in_channel(url, user_id, token, channel_id):
    datain = {"token": token, "channel_id": channel_id}
    channel_members = requests.get(url+ "channel/details", params=datain).json()['all_members']

    return len(list(filter(lambda user: user_id == user['u_id'], channel_members)))


def test_join_basic(url, initialise_user_data, initialise_channel_data):
    '''
    basic test with no edge cases or errors raised
    '''
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
    '''
    check that channel_join raises InputError
    if channel_id does not refer to a valid channel
    '''
    join_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": -1
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert response.status_code == 400

def test_join_private_user(url, initialise_user_data, initialise_channel_data):
    '''
    check that channel_join raises AccessError
    if channel_id refers to a channel that is private
    (when the authorised user is not a global owner)
    '''
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
    '''
    check that global owners can join private channels
    '''
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
    '''
    check that channel_join raises AccessError
    if token is invalid
    '''
    join_input = {
        "token": " ",
        "channel_id": initialise_channel_data['admin_publ']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)

    assert response.status_code == 400

def test_join_already_member(url, initialise_user_data, initialise_channel_data):
    '''
    check that users can join a channel they are already in
    '''
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

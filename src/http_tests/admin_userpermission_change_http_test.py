'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route(.....) return json.dumps({...})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> ...
'''

'''
EXCEPTIONS
Error type: InputError
    -> ..
Error type: AccessError
    -> ..
'''

# def test_url(url):
#     '''
#     A simple sanity test to check that the server is set up properly
#     '''
#     assert url.startswith("http")

def test_admin_userpermission_change_make_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['user1']['u_id']
    #Try get user1 to join private channel
    join_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": initialise_channel_data['admin_priv']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 400

    #make user0 admin
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 200

    #Now try get them to join channel
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 200

def test_admin_userpermission_change_remove_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['user1']['u_id']

    #make user0 admin
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)

    #try join private channel
    join_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": initialise_channel_data['admin_priv']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 200

    #now leave
    response = requests.post(url + "/channel/leave", json=join_input)
    assert response.status_code == 200

    #make them non-owner
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 2
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)

    #Try get user0 to join private channel
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 400

def test_admin_userpermission_change_remove_self(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['user1']['u_id']

    #make user0 admin
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 200

    #remove themselves as owner
    change_input = {
        "token": initialise_user_data['user1']['token'],
        "u_id": u_id,
        "permission_id": 2
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 200

    #try join private channel
    join_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": initialise_channel_data['admin_priv']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 400

def test_admin_userpermission_change_remove_last(url, initialise_user_data, initialise_channel_data):

    #Try remove themselves as admin - but unable as they are the only admin
    token = initialise_user_data['admin']['token']
    u_id = initialise_user_data['admin']['u_id']

    #make user0 admin
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 2
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 200
    #They can still join a prviate channel as they are the only admin
    join_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['user1_priv']['channel_id']
    }
    response = requests.post(url + "/channel/join", json=join_input)
    assert response.status_code == 200

def test_admin_userpermission_change_non_admin(url, initialise_user_data, initialise_channel_data):

    token = initialise_user_data['user1']['token']
    u_id = initialise_user_data['user1']['u_id']

    #try get user1 to make themselves admin
    change_input = {
        "token": token,
        "u_id": u_id,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

def test_admin_userpermission_change_invalid_permission_id(url, initialise_user_data, initialise_channel_data):

    change_input = {
        "token": initialise_user_data['admin']['token'],
        "u_id": initialise_user_data['user1']['u_id'],
        "permission_id": -1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

def test_admin_userpermission_change_invalid_uid(url, initialise_user_data, initialise_channel_data):

    change_input = {
        "token": initialise_user_data['admin']['token'],
        "u_id": -1,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

def test_admin_userpermission_change_invalid_token(url, initialise_user_data, initialise_channel_data):

    change_input = {
        "token": ' ',
        "u_id": initialise_user_data['user1']['u_id'],
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

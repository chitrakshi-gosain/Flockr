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
-> APP.route("/channel/leave", methods=['POST']) return
    json.dumps({})
-> APP.route("/admin/userpermission/change", methods=['POST']) return
    json.dumps({})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> u_id does not refer to a valid user
    -> permission_id does not refer to a value permission
Error type: AccessError
    -> authorised user is not an owner
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_admin_userpermission_change_make_admin(url, reset, initialise_user_data, initialise_channel_data):
    '''
    make user admin
    '''
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

def test_admin_userpermission_change_remove_admin(url, reset, initialise_user_data, initialise_channel_data):
    '''
    make user no longer admin
    '''
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

def test_admin_userpermission_change_remove_self(url, reset, initialise_user_data, initialise_channel_data):
    '''
    take away your own admin privileges
    '''
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

def test_admin_userpermission_change_remove_last(url, reset, initialise_user_data, initialise_channel_data):
    '''
    try to take away your own admin privileges
    when you are the only admin
    '''
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

def test_admin_userpermission_change_non_admin(url, reset, initialise_user_data, initialise_channel_data):
    '''
    attempt to make yourself an admin
    when you are not an admin
    '''
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

def test_admin_userpermission_change_invalid_permission_id(url, reset, initialise_user_data, initialise_channel_data):
    '''
    check that admin_userpermission_change raises InputError
    when permission_id is invalid
    '''
    change_input = {
        "token": initialise_user_data['admin']['token'],
        "u_id": initialise_user_data['user1']['u_id'],
        "permission_id": -1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

def test_admin_userpermission_change_invalid_uid(url, reset, initialise_user_data, initialise_channel_data):
    '''
    check that admin_userpermission_change raises InputError
    when u_id is invalid
    '''
    change_input = {
        "token": initialise_user_data['admin']['token'],
        "u_id": -1,
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

def test_admin_userpermission_change_invalid_token(url, reset, initialise_user_data, initialise_channel_data):
    '''
    check that admin_userpermission_change raises AccessError
    when token is invalid
    '''
    change_input = {
        "token": ' ',
        "u_id": initialise_user_data['user1']['u_id'],
        "permission_id": 1
    }
    response = requests.post(url + "/admin/userpermission/change", json=change_input)
    assert response.status_code == 400

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

Iteration 3
'''

import requests
import time

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return json.dumps({channel_id})
-> APP.route("/channel/join", methods=['POST']) return json.dumps({})
-> APP.route("/standup/start", methods=['POST']) return json.dumps({})

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
Error type: AccessError
    -> token passed in is not a valid token
Error type: InputError
    -> channel ID is not a valid channel
'''

def test_standup_active_expiry(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #start standup
    start_response = requests.post(url + "/standup/start", json={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    }).json()

    active_input = {
        'token': token,
        'channel_id': channel_id
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 200

    standup_info = active_response.json()
    assert standup_info['is_active']
    assert standup_info['time_finish'] == start_response['time_finish']

    time.sleep(1)

    #now standup has expired
    active_input = {
        'token': token,
        'channel_id': channel_id
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 200

    standup_info = active_response.json()
    assert not standup_info['is_active']
    assert standup_info['time_finish'] == None

def test_standup_active_invalid_token(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #start standup
    requests.post(url + "/standup/start", json={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })

    active_input = {
        'token': ' ',
        'channel_id': channel_id
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 400

def test_standup_active_invalid_channel(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #start standup
    requests.post(url + "/standup/start", json={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })

    active_input = {
        'token': token,
        'channel_id': -1
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 400

def test_standup_active_no_standup(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    active_input = {
        'token': token,
        'channel_id': channel_id
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 200

    standup_info = active_response.json()
    assert not standup_info['is_active']
    assert standup_info['time_finish'] == None

def test_standup_active_not_in_channel(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    user_token = initialise_user_data['user0']['token'] # not in standup channel
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    #start standup
    start_response = requests.post(url + "/standup/start", json={
        'token': token,
        'channel_id': channel_id,
        'length': 100
    }).json()

    active_input = {
        'token': user_token,
        'channel_id': channel_id
    }
    active_response = requests.get(url + "/standup/active", params=active_input)
    assert active_response.status_code == 200

    standup_info = active_response.json()
    assert standup_info['is_active']
    assert standup_info['time_finish'] == start_response['time_finish']

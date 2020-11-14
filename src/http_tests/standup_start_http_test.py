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
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
-> APP.route("/standup/active", methods=['GET']) return
    json.dumps({})
-> APP.route("/standup/send", methods=['POST']) return
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
Error type: AccessError
    -> token passed in is not a valid token
Error type: InputError
    -> channel ID is not a valid channel
    -> an active standup is currently running in this channel
'''

def test_standup_start_basic(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel1_id = initialise_channel_data['admin_publ']['channel_id']
    channel2_id = initialise_channel_data['admin_priv']['channel_id']

    start_input = {
        'token': token,
        'channel_id': channel1_id,
        'length': 1
    }
    start_response1 = requests.post(url + "/standup/start", json=start_input)
    assert start_response1.status_code == 200

    start_input = {
        'token': token,
        'channel_id': channel2_id,
        'length': 100
    }
    start_response2 = requests.post(url + "/standup/start", json=start_input)
    assert start_response2.status_code == 200

    time.sleep(1)
    standup1_status = requests.get(url + "/standup/active", params={
        'token': token,
        'channel_id': channel1_id
    }).json()

    standup2_status = requests.get(url + "/standup/active", params={
        'token': token,
        'channel_id': channel2_id
    }).json()

    assert not standup1_status['is_active']
    assert standup2_status['is_active']

    send_response = requests.post(url + "/standup/send", json={
        'token': token,
        'channel_id': channel1_id,
        'message': 'standup1 expired'
    })
    assert send_response.status_code == 400

    send_response = requests.post(url + "/standup/send", json={
        'token': token,
        'channel_id': channel2_id,
        'message': 'standup2 still valid'
    })
    assert send_response.status_code == 200

def test_standup_start_invalid_token(url, initialise_channel_data):
    invalid_token = ' '
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    start_input = {
        'token': invalid_token,
        'channel_id': channel_id,
        'length': duration
    }
    start_response = requests.post(url+ "/standup/start", json=start_input)
    assert start_response.status_code == 400

def test_standup_start_invalid_channel(url, initialise_user_data):
    token = initialise_user_data['admin']['token']
    invalid_channel_id = -1
    duration = 1

    start_input = {
        'token': token,
        'channel_id': invalid_channel_id,
        'length': duration
    }
    start_response = requests.post(url+ "/standup/start", json=start_input)
    assert start_response.status_code == 400

def test_standup_start_already_running(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 100

    start_input = {
        'token': token,
        'channel_id': channel_id,
        'length': duration
    }
    start_response = requests.post(url+ "/standup/start", json=start_input)
    assert start_response.status_code == 200

    start_response = requests.post(url+ "/standup/start", json=start_input)
    assert start_response.status_code == 400

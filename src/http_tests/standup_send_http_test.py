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
    -> the authorised user is not a member of the channel that the
       message is within
Error type: InputError
    -> channel ID is not a valid channel
    -> message is more than 1000 characters
    -> an active standup is not currently running in this channel
'''

def is_message_in_messages(str_message, messages):
    for message in messages:
        if str_message == message['message']:
            return True
    return False

def test_standup_send_basic(url, initialise_user_data, initialise_channel_data):
    token1 = initialise_user_data['admin']['token']
    token2 = initialise_user_data['user1']['token']
    channel1_id = initialise_channel_data['admin_publ']['channel_id']
    channel2_id = initialise_channel_data['user1_priv']['channel_id']
    duration = 5

    #user1 join channel
    requests.post(url + '/channel/join', json={
        'token': token2,
        'channel_id': channel1_id
    })

    #start standups
    requests.post(url + '/standup/start', json={ #admin_publ
        'token': token1,
        'channel_id': channel1_id,
        'length': duration
    })

    requests.post(url + '/standup/start', json={ #user1_publ
        'token': token2,
        'channel_id': channel2_id,
        'length': duration
    })

    #send messages
    send_input = {
        'token': token1,
        'channel_id': channel1_id,
        'message': 'start of standup in admin_publ'
    }
    send_response = requests.post(url +'/standup/send', json=send_input)
    assert send_response.status_code == 200

    send_input = {
        'token': token2,
        'channel_id': channel1_id,
        'message': 'end of standup in admin_publ'
    }
    send_response = requests.post(url +'/standup/send', json=send_input)
    assert send_response.status_code == 200

    send_input = {
        'token': token2,
        'channel_id': channel2_id,
        'message': 'start of standup in user1_publ'
    }
    send_response = requests.post(url +'/standup/send', json=send_input)
    assert send_response.status_code == 200

    #wait 1 seconds for standups to expire (and call standup_active() to update)
    time.sleep(5)
    requests.get(url +'/standup/active', params={
        'token': token1,
        'channel_id': channel1_id
    })

    requests.get(url +'/standup/active', params={
        'token': token1,
        'channel_id': channel2_id
    })

    #try send message with standup expired
    send_input = {
        'token': token1,
        'channel_id': channel1_id,
        'message': 'standup has expired'
    }
    send_response = requests.post(url +'/standup/send', json=send_input)
    assert send_response.status_code == 400

    admin_publ_standup_message = 'admin_first: start of standup in admin_publ\n' +\
                                 'user1_first: end of standup in admin_publ'
    user1_publ_standup_message = 'user1_first: start of standup in user1_publ'

    #get channel_messages
    admin_publ_messages = requests.get(url + '/channel/messages', params={
        'token': token1,
        'channel_id': channel1_id,
        'start': 0
    }).json()
    user1_publ_messages = requests.get(url + '/channel/messages', params={
        'token': token2,
        'channel_id': channel2_id,
        'start': 0
    }).json()

    assert is_message_in_messages(admin_publ_standup_message, admin_publ_messages['messages'])
    assert is_message_in_messages(user1_publ_standup_message, user1_publ_messages['messages'])


def test_standup_send_invalid_token(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 100

    requests.post(url + '/standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': duration
    })

    send_input = {
        'token': ' ',
        'channel_id': channel_id,
        'message': 'sent with invalid token'
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

def test_standup_send_not_in_channel(url, initialise_user_data, initialise_channel_data):
    standup_token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_priv']['channel_id']
    duration = 100

    requests.post(url + '/standup/start', json={
        'token': standup_token,
        'channel_id': channel_id,
        'length': duration
    })

    message_token = initialise_user_data['user1']['token']
    send_input = {
        'token': message_token,
        'channel_id': channel_id,
        'message': 'I am not in this channel'
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

def test_standup_send_invalid_channel(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 100

    requests.post(url + '/standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': duration
    })

    send_input = {
        'token': token,
        'channel_id': -1,
        'message': 'sent with invalid channel_id'
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

def test_standup_send_long_short_message(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 100

    requests.post(url + '/standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': duration
    })

    send_input = {
        'token': token,
        'channel_id': channel_id,
        'message': 'aa'*1000
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

    send_input = {
        'token': token,
        'channel_id': channel_id,
        'message': ''
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

def test_standup_send_not_active(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    send_input = {
        'token': token,
        'channel_id': channel_id,
        'message': 'there is no standup'
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 400

def test_standup_send_expire_leave(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 5

    requests.post(url + '/standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': duration
    })

    send_input = {
        'token': token,
        'channel_id': channel_id,
        'message': 'I am about to logout'
    }
    send_response = requests.post(url + '/standup/send', json=send_input)
    assert send_response.status_code == 200

    requests.post(url + '/auth/logout', json={
        'token': token
    })

    #we still need a valid token
    user_token = initialise_user_data['user1']['token']
    requests.post(url + '/channel/join', json={
        'token': user_token,
        'channel_id': channel_id
    })

    #make sure message is still sent at end
    time.sleep(5)
    requests.get(url +'/standup/active', params={
        'token': user_token,
        'channel_id': channel_id
    })

    message = 'admin_first: I am about to logout'
    admin_publ_messages = requests.get(url + '/channel/messages', params={
        'token': user_token,
        'channel_id': channel_id,
        'start': 0
    }).json()

    assert is_message_in_messages(message, admin_publ_messages['messages'])

def test_standup_send_no_messages(url, initialise_user_data, initialise_channel_data):
    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    duration = 1

    requests.post(url + '/standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': duration
    })

    time.sleep(1)
    requests.get(url +'/standup/active', params={
        'token': token,
        'channel_id': channel_id
    })

    #should send nothing
    messages = requests.get(url + '/channel/messages', params={
        'token': token,
        'channel_id': channel_id,
        'start': 0
    }).json()

    assert messages['messages'] == []

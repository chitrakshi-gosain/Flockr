'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 3
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
-> APP.route("/message/send", methods=['POST']) return
    json.dumps({message_id})
-> APP.route("/message/edit", methods=['PUT']) return
    json.dumps({})
-> APP.route("/message/react", methods=['POST']) return
    json.dumps({})
-> APP.route("/message/unreact", methods=['POST']) return
    json.dumps({})
-> APP.route("/search", methods=['GET']) return
    json.dumps({messages})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS:
Error type: AccessError
    -> token passed in is not a valid token
Error type: InputError
    -> message_id is not a valid message within a channel that the
        authorised user has joined
    -> react_id is not a valid React ID
    -> Message with ID message_id does not contain an active React
        with ID react_id from the authorised user
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def message_details(url, token, message_id):
    # 'search' with empty query string returns list of all messages
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    message_list = search_response.json()['messages']    
    for message in message_list:
        if message['message_id'] == message_id:
            return message
    return False

def react_details(url, token, message_id, react_id):
    message = message_details(url, token, message_id)
    for react in message['reacts']:
        if react['react_id'] == react_id:
            return react
    return False

def test_http_message_unreact_noerrors(url, initialise_user_data, initialise_channel_data):
    '''
    basic test with no edge case or errors raised
    '''

    # get user data
    user_details = initialise_user_data['admin']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # send message
    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': "Test message"
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react_response = requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_react_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # user unreacts to their own message
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']

def test_http_message_unreact_invalidmessage(url, initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if message_id is not a valid message within a channel that the authorised user has joined
    '''

    # get user data
    user_details = initialise_user_data['admin']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # send message
    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': "Test message"
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react_response = requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_react_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set message_id as -1
    message_id = -1
    # unreact - assert InputError
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 400

def test_http_message_unreact_invalidreact(url, initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if react_id is not a valid React ID
    '''

    # get user data
    user_details = initialise_user_data['admin']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # send message
    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': "Test message"
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # react
    message_react_response = requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_react_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set react_id as -1
    react_id = -1
    # unreact - assert InputError
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 400

def test_http_message_unreact_twice(url, initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if message with ID message_id does not contain an active React with ID react_id from the authorised user 
    '''

    # get user data
    user_details = initialise_user_data['admin']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # send message
    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': "Test message"
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # react
    message_react_response = requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_react_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # unreact
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # unreact - assert InputError
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 400

def test_http_message_unreact_notauth(url, initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises AccessError
    if token is invalid
    '''

    # get user data
    user_details = initialise_user_data['admin']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['admin_publ']['channel_id']
    # send message
    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': "Test message"
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # react
    message_react_response = requests.post(f"{url}/message/react", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_react_response.status_code == 200
    # get reaction details for message with message_id
    react = react_details(url, token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set token as ' '
    token = ' '
    # unreact - assert AccessError
    message_unreact_response = requests.post(f"{url}/message/unreact", json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })
    assert message_unreact_response.status_code == 400

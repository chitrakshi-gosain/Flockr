'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

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
-> APP.route("/message/send", methods=['POST']) return
    json.dumps({message_id})
-> APP.route("/message/edit", methods=['PUT']) return
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
EXCEPTIONS
Error type: AccessError
    -> user (based on token) is not sender of message with message_id
    -> token is not valid
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_http_message_edit_no_errors(initialise_channel_data, initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    # assert message_dict contains the original message
    for message_dict in messages:
        if message_dict['message_id'] == message_id:
            assert message_dict['message'] == first_message
            break

    second_message = "This is the edited message."

    message_edit_response = requests.put(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': second_message
    })
    assert message_edit_response.status_code == 200

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    # assert message_dict contains the edited message
    for message_dict in messages:
        if message_dict['message_id'] == message_id:
            assert message_dict['message'] == second_message
            break

def test_http_message_edit_secondmessage(initialise_channel_data, initialise_user_data, url):
    '''
    edits the second sent message, not the first
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    first_message0 = "This is the first original message."
    first_message1 = "This is the second original message."

    message_send_response0 = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message0
    })
    assert message_send_response0.status_code == 200
    message_id0 = message_send_response0.json()["message_id"]

    message_send_response1 = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message1
    })
    assert message_send_response1.status_code == 200
    message_id1 = message_send_response1.json()["message_id"]

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    for message_dict in messages:
        if message_dict['message_id'] == message_id0:
            assert message_dict['message'] == first_message0
            break

    for message_dict in messages:
        if message_dict['message_id'] == message_id1:
            assert message_dict['message'] == first_message1
            break

    second_message1 = "This is the second edited message."

    message_edit_response1 = requests.put(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id1,
        'message': second_message1
    })
    assert message_edit_response1.status_code == 200

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    for message_dict in messages:
        if message_dict['message_id'] == message_id1:
            assert message_dict['message'] == second_message1
            break

def test_http_message_edit_emptystring(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit deletes the message
    if provided with an empty string
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    # assert message_dict contains the original message
    for message_dict in messages:
        if message_dict['message_id'] == message_id:
            assert message_dict['message'] == first_message
            break

    second_message = ""

    message_edit_response = requests.put(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': second_message
    })
    assert message_edit_response.status_code == 200

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']
    assert message_id not in [message['message_id'] for message in messages]

def test_http_message_edit_notsender(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    token_admin = admin['token']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    token0 = user0['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user0 joins channel, therefore is a member but not an owner
    channel_join_response = requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })
    assert channel_join_response.status_code == 200

    first_message = "This is the original message."

    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token_admin,
        'channel_id': channel_id,
        'message': first_message
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token_admin,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    # assert message_dict contains the original message
    for message_dict in messages:
        if message_dict['message_id'] == message_id:
            assert message_dict['message'] == first_message
            break

    second_message = "This is the edited message."

    # user0 did not send the message with message_id, so token0 should fail
    # assert that channel_addowner returns status code 400 (indicating user error)
    message_edit_response = requests.put(f"{url}/message/edit", json={
        'token': token0,
        'message_id': message_id,
        'message': second_message
    })
    assert message_edit_response.status_code == 400

def test_http_message_edit_invalidtoken(initialise_channel_data, initialise_user_data, url):
    '''
    test that message_edit raises AccessError if the provided token is not valid
    '''

    user = initialise_user_data['admin']
    token = user['token']

    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    first_message = "This is the original message."

    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]

    # search using empty query string, thus return list of every message
    search_response = requests.get(f"{url}/search", params={
        'token': token,
        'query_str': ""
    })
    assert search_response.status_code == 200
    messages = search_response.json()['messages']

    # assert message_dict contains the original message
    for message_dict in messages:
        if message_dict['message_id'] == message_id:
            assert message_dict['message'] == first_message
            break

    second_message = "This is the edited message."

    # assume " " is not a valid token
    token = " "

    # assert that channel_addowner returns status code 400 (indicating user error)
    message_edit_response = requests.put(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': second_message
    })
    assert message_edit_response.status_code == 400

def test_message_edit_invalid_size(url, initialise_user_data, initialise_channel_data):
    '''
    Test that messages cannot be larger than 1000 characters
    '''
    user_details = initialise_user_data['admin']
    token = user_details['token']

    channel_id = initialise_channel_data['admin_publ']['channel_id']

    first_message = "This is the original message."

    message_send_response = requests.post(f"{url}/message/send", json={
        'token': token,
        'channel_id': channel_id,
        'message': first_message,
    })
    assert message_send_response.status_code == 200
    message_id = message_send_response.json()["message_id"]

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    assert requests.put(f"{url}/message/edit", json={
        'token': token,
        'message_id': message_id,
        'message': message,
    }).status_code == 400
'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 2
'''

import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/message/send", methods=['POST']) return
   json.dumps({token, channel_id, message})
-> APP.route("/channel/join", methods=['POST']) return json.dumps({})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
-> APP.route("/channel/messages", methods=['GET']) return
    json.dumps({messages, start, end})
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
Error Type: InputError
    -> Channel ID is not a valid channel
Error Type: AccessError
    -> channel_id refers to a channel that is private (when the authorised user is not a global owner)
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def get_messages(url, admin_token):
    messages = requests.get(url + "/search", params = {
        "token": admin_token,
        "query_str": ""
    }).json()
    return messages

def test_user_not_authorised(url, reset, initialise_user_data, initialise_channel_data):

    send_input = {
        "token": initialise_user_data['user1']['token'],
        "channel_id": initialise_channel_data['admin_priv']['channel_id'],
        "message": "Sample message"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 400


def test_channel_id_not_valid(url, reset, initialise_user_data, initialise_channel_data):

    send_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": -1,
        "message": "Sample message"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 400


def test_token_invalid(url, reset, initialise_user_data, initialise_channel_data):

    send_input = {
        "token": " ",
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "Sample message"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 400

def test_return_type(url, reset, initialise_user_data, initialise_channel_data):

    send_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "Sample message"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 200

    messages = get_messages(url, initialise_user_data['admin']['token'])
    assert isinstance(messages['messages'], list)
    assert isinstance(messages['messages'][0], dict)
    assert isinstance(messages['messages'][0]['message_id'], int)
    assert isinstance(messages['messages'][0]['u_id'], int)
    assert isinstance(messages['messages'][0]['message'], str)
    assert isinstance(messages['messages'][0]['message'], object)

def test_sample(url, reset, initialise_user_data, initialise_channel_data):
    #join channel
    requests.post(url + "/channel/join", json={
        "token": initialise_user_data['user1']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id']
    })
    # admin message1
    send_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "Hey, how are you"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 200

    # user1 message1
    send_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "Good thank you, how are you!"
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 200
    message_id = response.json()

    # admin message 2
    send_input = {
        "token": initialise_user_data['admin']['token'],
        "channel_id": initialise_channel_data['admin_publ']['channel_id'],
        "message": "Very well, thanks."
    }
    response = requests.post(url + "/message/send", json=send_input)
    assert response.status_code == 200

    messages = get_messages(url, initialise_user_data['admin']['token'])
    for message in messages['messages']:
         if message['message_id'] == message_id['message_id']:
             assert message['message'] == "Good thank you, how are you!"

def test_invalid_size(url, reset, initialise_user_data, initialise_channel_data):
    '''
    Testing with a message that is too large
    '''

    users = initialise_user_data
    channels = initialise_channel_data

    requests.post(url + "/channel/join", json={
        "token": users['user0']['token'],
        "channel_id": channels['owner_publ']['channel_id']
    })

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    assert requests.post(url + "/message/send", json={
        'token': users['user0']['token'],
        'channel_id': channels['owner_publ']['channel_id'],
        'message': message,
    }).status_code == 400
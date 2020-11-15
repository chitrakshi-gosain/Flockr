'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

Iteration 3
'''

import time
from datetime import timezone, datetime, timedelta
import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/message/sendlater", methods=['POST']) return
   json.dumps({message_id})
-> APP.route("/auth/logout", methods=['POST']) return
   json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> Channel ID is not a valid channel
    -> Message is more than 1000 characters
    -> Time sent is a time in the past
Error type: AccessError
    -> token passed in is not a valid token
    -> The authorised user has not joined the channel they are trying
       to post to
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_message_sendlater_valid(url, initialise_user_data, initialise_channel_data):
    '''
    Testing a basic valid case
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=2)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    message_id = requests.post(f'{url}/message/sendlater', json={
        'token': users['owner']['token'],
        'channel_id': channels['owner_publ']['channel_id'],
        'message': 'Hello World!',
        'time_sent': time_sent,
    }).json()

    time.sleep(3)

    assert isinstance(message_id['message_id'], int)

def test_message_sendlater_id_invalid(url, initialise_user_data):
    '''
    Testing with an invalid channel_id
    '''
    users = initialise_user_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    assert requests.post(f'{url}/message/sendlater', json={
        'token': users['owner']['token'],
        'channel_id': 0,
        'message': 'Hello World!',
        'time_sent': time_sent,
    }).status_code == 400

def test_message_sendlater_large_invalid(url, initialise_user_data, initialise_channel_data):
    '''
    Testing with a message that is too large
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    assert requests.post(f'{url}/message/sendlater', json={
        'token': users['owner']['token'],
        'channel_id': channels['owner_publ']['channel_id'],
        'message': message,
        'time_sent': time_sent,
    }).status_code == 400

def test_message_sendlater_time_invalid(url, initialise_user_data, initialise_channel_data):
    '''
    Testing with an invalid time in the past
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time - timedelta(minutes=10)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    assert requests.post(f'{url}/message/sendlater', json={
        'token': users['owner']['token'],
        'channel_id': channels['owner_publ']['channel_id'],
        'message': 'Hello World!',
        'time_sent': time_sent,
    }).status_code == 400

def test_message_sendlater_channel_invalid(url, initialise_user_data, initialise_channel_data):
    '''
    Testing with a channel that the user is not a member of
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    assert requests.post(f'{url}/message/sendlater', json={
        'token': users['user0']['token'],
        'channel_id': channels['admin_publ']['channel_id'],
        'message': 'Hello World!',
        'time_sent': time_sent,
    }).status_code == 400

def test_message_sendlater_token_invalid(url, initialise_user_data, initialise_channel_data):
    '''
    Testing with an invalid token
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    invalid_token = users['user0']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    assert requests.post(f'{url}/message/sendlater', json={
        'token': invalid_token,
        'channel_id': channels['owner_publ']['channel_id'],
        'message': 'Hello World!',
        'time_sent': time_sent,
    }).status_code == 400
'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 3
'''

import time
from datetime import timezone, datetime, timedelta
import pytest
from auth import auth_logout
from message import message_sendlater
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> message_sendlater(token, channel_id, message, time_sent) return
   {message_id}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
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

def test_message_sendlater_valid(initialise_user_data, initialise_channel_data):
    '''
    Testing a basic valid case
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=2)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    message_id = message_sendlater(users['user0']['token'], channels['user0_publ']['channel_id'], 
        'Hello World!', time_sent)

    time.sleep(3)

    assert isinstance(message_id['message_id'], int)

def test_message_sendlater_id_invalid(initialise_user_data):
    '''
    Testing with an invalid channel_id
    '''
    users = initialise_user_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    with pytest.raises(InputError):
        message_sendlater(users['user0']['token'], 0, 'Hello World!', time_sent)

def test_message_sendlater_large_invalid(initialise_user_data, initialise_channel_data):
    '''
    Testing with a message that is too large
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    with pytest.raises(InputError):
        message_sendlater(users['user0']['token'], channels['user0_publ']['channel_id'], 
        message, time_sent)

def test_message_sendlater_time_invalid(initialise_user_data, initialise_channel_data):
    '''
    Testing with an invalid time in the past
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time - timedelta(minutes=10)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    with pytest.raises(InputError):
        message_sendlater(users['user0']['token'], channels['user0_publ']['channel_id'], 
        'Hello World!', time_sent)

def test_message_sendlater_channel_invalid(initialise_user_data, initialise_channel_data):
    '''
    Testing with a channel that the user is not a member of
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    with pytest.raises(AccessError):
        message_sendlater(users['user0']['token'], channels['admin_publ']['channel_id'], 
        'Hello World!', time_sent)

def test_message_sendlater_token_invalid(initialise_user_data, initialise_channel_data):
    '''
    Testing with an invalid token
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now(timezone.utc)
    date_sent = curr_time + timedelta(seconds=30)
    time_sent = date_sent.replace(tzinfo=timezone.utc).timestamp()

    invalid_token = users['user0']['token']
    auth_logout(invalid_token)

    with pytest.raises(AccessError):
        message_sendlater(invalid_token, channels['user0_publ']['channel_id'], 
        'Hello World!', time_sent)
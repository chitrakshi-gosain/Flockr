'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

Iteration 2
'''

import pytest
from channel import channel_join
from message import message_send
from other import search
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, firstname, lastname)
-> channels_create(token) return {channel_id}
-> message_send(token, channel_id, message) return {message_id}
-> channel_join(token, channel_id) return {}
-> search(token, query_str) return {messages}
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
    -> channel_id does not refer to a valid channel
    -> token passed in is not a valid token
    -> u_id does not refer to a valid user
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
'''

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages

def test_user_not_authorised(initialise_user_data, initialise_channel_data):

    channel1_id = initialise_channel_data['owner_priv']
    user1_credentials = initialise_user_data['user1']      
    with pytest.raises(AccessError):
        message_send(user1_credentials['token'], channel1_id['channel_id'], "Sample message")


def test_channel_id_not_valid(initialise_user_data):
    owner_credentials = initialise_user_data['owner']
    invalid_channel_id = -1
    with pytest.raises(InputError):
        message_send(owner_credentials['token'], invalid_channel_id, "Sample message")


def test_token_invalid(initialise_channel_data):

    channel1_id = initialise_channel_data['owner_priv']
    with pytest.raises(AccessError):
        message_send('incorrect_user1_token', channel1_id['channel_id'], "Sample message")

def test_return_type(initialise_user_data, initialise_channel_data):
    owner_credentials = initialise_user_data['owner']

    channel1_id = initialise_channel_data['owner_priv']
    message_send(owner_credentials['token'], channel1_id['channel_id'], "Sample message")

    admin_token = owner_credentials['token']
    messages = get_messages(admin_token)
    assert isinstance(messages['messages'], list)
    assert isinstance(messages['messages'][0], dict)
    assert isinstance(messages['messages'][0]['message_id'], int)
    assert isinstance(messages['messages'][0]['u_id'], int)
    assert isinstance(messages['messages'][0]['message'], str)
    assert isinstance(messages['messages'][0]['message'], object)

def test_sample(initialise_user_data, initialise_channel_data):
    
    channel1_id = initialise_channel_data['owner_publ']
    owner_credentials = initialise_user_data['owner']
    user1_credentials = initialise_user_data['user1']                                 # create a public channel
    channel_join(user1_credentials['token'], channel1_id['channel_id'])

    message_send(owner_credentials['token'], channel1_id['channel_id'], "Hey, how are you")
    message_id = message_send(user1_credentials['token'], channel1_id['channel_id'], "Good thank you, how are you!")
    message_send(owner_credentials['token'], channel1_id['channel_id'], "Very well, thanks.")

    admin_token = owner_credentials['token']
    messages = get_messages(admin_token)
    for message in messages['messages']:
        if message['message_id'] == message_id['message_id']:
            assert message['message'] == "Good thank you, how are you!"

def test_invalid_size(initialise_user_data, initialise_channel_data):
    '''
    Testing with a message that is too large
    '''

    users = initialise_user_data
    channels = initialise_channel_data

    channel_join(users['user0']['token'], channels['user0_publ']['channel_id'])

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    with pytest.raises(InputError):
        message_send(users['user0']['token'], channels['user0_publ']['channel_id'], message)

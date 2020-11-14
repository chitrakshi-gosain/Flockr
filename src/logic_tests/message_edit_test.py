'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 2
'''

import pytest
from channel import channel_join
from message import message_send, message_edit
from error import AccessError, InputError
from other import search

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channels_create(token, name, is_public) return {channel_id}
-> channel_join(token, channel_id) return {}
-> message_send(token, channel_id, message) return {}
-> message_edit(token, message_id, message) return {message_id}
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
Error type: AccessError
    -> user (based on token) is not sender of message with message_id
    -> token is not valid
'''

'''
KEEP IN MIND:
-> channels_create adds user (based on token) as member and owner of the channel
'''

def get_messages(admin_token):
    messages = search(admin_token, '')
    return messages

def message_details(token, message_id):
    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            return message
    return False

def test_message_edit_noerrors(initialise_user_data, initialise_channel_data):
    '''
    basic test with no edge case or errors raised
    '''

    # 'user' with u_id and token is the first to register, thus also admin of the flockr
    user_details = initialise_user_data['user0']
    token = user_details['token']

    channel_id = initialise_channel_data['user0_publ']['channel_id']

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]

    # get dictionary containing message_id, u_id, message, time_created
    message = message_details(token, message_id)
    assert message['message'] == first_message

    second_message = "This is the edited message."

    message_edit(token, message_id, second_message)

    # assert message has changed
    message = message_details(token, message_id)
    assert message['message'] == second_message

def test_message_edit_secondmessage(initialise_user_data, initialise_channel_data):
    '''
    edits the second sent message, not the first
    '''

    # 'user' with u_id and token is the first to register, thus also admin of the flockr
    user_details = initialise_user_data['user0']
    token = user_details['token']

    channel_id = initialise_channel_data['user0_publ']['channel_id']

    first_message0 = "This is the first original message."
    first_message1 = "This is the second original message."

    message_info0 = message_send(token, channel_id, first_message0)
    message_id0 = message_info0["message_id"]

    message0 = message_details(token, message_id0)
    assert message0['message'] == first_message0

    message_info1 = message_send(token, channel_id, first_message1)
    message_id1 = message_info1["message_id"]

    message1 = message_details(token, message_id1)
    assert message1['message'] == first_message1
    
    second_message1 = "This is the second edited message."

    message_edit(token, message_id1, second_message1)

    message1 = message_details(token, message_id1)
    assert message1['message'] == second_message1

def test_message_edit_emptystring(initialise_user_data, initialise_channel_data):
    '''
    test that message_edit deletes the message
    if provided with an empty string
    '''

    # 'user' with u_id and token is the first to register, thus also admin of the flockr
    user_details = initialise_user_data['user0']
    token = user_details['token']

    channel_id = initialise_channel_data['user0_publ']['channel_id']

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]

    # get dictionary containing message_id, u_id, message, time_created
    message = message_details(token, message_id)
    assert message['message'] == first_message

    second_message = ""

    message_edit(token, message_id, second_message)

    # message_details returns False if message does not exist
    # therefore assert message == False
    message = message_details(token, message_id)
    assert not message

def test_message_edit_notsender(initialise_user_data, initialise_channel_data):
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = initialise_user_data['user0']
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = initialise_user_data['user1']
    token1 = user1_details['token']

    # channel with channel_id has members user0, user1 and owner user0
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    channel_join(user1_details['token'], channel_id)

    first_message = "This is the original message."

    message_info = message_send(token0, channel_id, first_message)
    message_id = message_info["message_id"]

    message = message_details(token0, message_id)
    assert message['message'] == first_message

    second_message = "This is the edited message."

    # user1 did not send the original message, so token1 should fail
    with pytest.raises(AccessError):
        message_edit(token1, message_id, second_message)

def test_message_edit_notauth(initialise_user_data, initialise_channel_data):
    '''
    test that message_edit raises AccessError
    if token is invalid
    '''

    # 'user' with u_id and token is the first to register, thus also admin of the flockr
    user_details = initialise_user_data['user0']
    token = user_details['token']

    channel_id = initialise_channel_data['user0_publ']['channel_id']

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]

    # get dictionary containing message_id, u_id, message, time_created
    message = message_details(token, message_id)
    assert message['message'] == first_message

    second_message = "This is the edited message."

    # assume " " is not a valid token
    token = " "

    with pytest.raises(AccessError):
        message_edit(token, message_id, second_message)

def test_message_edit_invalid_size(initialise_user_data, initialise_channel_data):
    '''
    Test that messages cannot be larger than 1000 characters
    '''
    user_details = initialise_user_data['user0']
    token = user_details['token']

    channel_id = initialise_channel_data['user0_publ']['channel_id']

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]

    # get dictionary containing message_id, u_id, message, time_created
    message = message_details(token, message_id)
    assert message['message'] == first_message

    message = 'djsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergdjsfgnpoarkegnalknosndkbnsnrlinpogaijonfvljgblaonewojifoanvkdnslbnmv,x.vnb;n[ojgoarpirhgoanfapo;jfigushbefkbnviuseboriguapiergkjabljgblsdblgibspirhgangkljsdbflbnpsnbksljbrihapiruhgperhisbdhfjbnbksnlbhpisurhgoawnrkjfbsdljbishorngabrghbaoirughsdbhsfugbarebgnjhsbgkbsbhisbdrgkjhbasoirufhapnoiaebrpigusdkjfbvnjdfbnuisrjpofjapoenfposrngpisdpgijprfnvindpishuprogjsikjdrnvuishporghpaierfoiuehpouvhisdbniusebrgpauhjfpjnfsdlkbnsdpifugjpoierjgnsdivfuhnpsuidhpishnrpgouhjsdpofigjsidnffghsergsfgbhdrtstrhsdfwwergsdfhsdhsdh'

    with pytest.raises(InputError):
        message_edit(token, message_id, message)

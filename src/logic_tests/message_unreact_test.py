'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 3
'''

import pytest
from message import message_send, message_react, message_unreact
from error import InputError, AccessError
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
-> message_react(token, message_id, react_id) return {}
-> message_unreact(token, message_id, react_id) return {}
-> search(token, query_str) return {messages}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
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

'''
KEEP IN MIND:
-> channels_create adds user (based on token) as member and owner of the channel
'''

def message_details(token, message_id):
    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            return message
    return False

def react_details(token, message_id, react_id):
    message = message_details(token, message_id)
    for react in message['reacts']:
        if react['react_id'] == react_id:
            return react
    return False

def test_message_unreact_noerrors(initialise_user_data, initialise_channel_data):
    '''
    basic test with no edge case or errors raised
    '''

    # get user data
    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    # send message
    message_id = message_send(token, channel_id, "Test message")['message_id']
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # user unreacts to their own message
    message_unreact(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']

def test_message_unreact_invalidmessage(initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if message_id is not a valid message within a channel that the authorised user has joined
    '''

    # get user data
    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    # send message
    message_id = message_send(token, channel_id, "Test message")['message_id']
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set message_id as -1
    message_id = -1
    # unreact - assert InputError
    with pytest.raises(InputError):
        message_unreact(token, message_id, react_id)

def test_message_unreact_invalidreact(initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if react_id is not a valid React ID
    '''

    # get user data
    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    # send message
    message_id = message_send(token, channel_id, "Test message")['message_id']
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set react_id as -1
    react_id = -1
    # unreact - assert InputError
    with pytest.raises(InputError):
        message_unreact(token, message_id, react_id)

def test_message_unreact_twice(initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises InputError
    if message with ID message_id does not contain an active React with ID react_id from the authorised user 
    '''

    # get user data
    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    # send message
    message_id = message_send(token, channel_id, "Test message")['message_id']
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # react
    message_react(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # unreact
    message_unreact(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # unreact - assert InputError
    with pytest.raises(InputError):
        message_unreact(token, message_id, react_id)

def test_message_unreact_notauth(initialise_user_data, initialise_channel_data):
    '''
    test that message_unreact raises AccessError
    if token is invalid
    '''

    # get user data
    user_details = initialise_user_data['user0']
    u_id, token = user_details['u_id'], user_details['token']
    # get channel data
    # channel has member and owner user
    channel_id = initialise_channel_data['user0_publ']['channel_id']
    # send message
    message_id = message_send(token, channel_id, "Test message")['message_id']
    # react_id 1 corresponds to 'thumbs up'
    react_id = 1
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message hasn't been reacted to
    assert u_id not in react['u_ids']
    assert not react['is_this_user_reacted']
    # user reacts to their own message
    message_react(token, message_id, react_id)
    # get reaction details for message with message_id
    react = react_details(token, message_id, react_id)
    # assert message has been reacted to
    assert u_id in react['u_ids']
    assert react['is_this_user_reacted']
    # set token as ' '
    token = ' '
    # unreact - assert AccessError
    with pytest.raises(AccessError):
        message_unreact(token, message_id, react_id)

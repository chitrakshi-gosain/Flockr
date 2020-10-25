from other import clear, search
from message import message_send
from auth import auth_register
from channels import channels_create
from channel import channel_join

import pytest
from error import InputError, AccessError

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> intialise_data() return { users }, { channels }
-> pop_datetimes(messages) return {messages} (without 'time_created')
-> test_other_search_not_in_channels()
-> test_other_search_join_channel()
-> test_other_search_no_messages()
-> test_other_search_empty_query()
-> test_other_search_admin()
-> test_other_search_multiple_channels()
-> test_other_search_invalid_token()
'''

'''
----search Documentation----

HTTP Method: GET

Parameters:(token, query_str)

Return type: { messages }

Exceptions: InputError ->
            AccessError ->

Description: Given a query string, return a collection of messages in
             all of the channels that the user has joined that match the query

'''

'''
Assumptions:
1. ' ' is an invalid token
2. Admins can see all messages
3. '' will return all visible messages
'''

def pop_datetimes(messages):
    for entry in messages:
        entry.pop('time_created')
    return messages

def test_other_search_not_in_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message_send(users['admin']['token'], channel_id, 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_join_channel(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    message1 = message_send(users['admin']['token'], channel_id, 'I am in no channels')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'I am in no channels',
    }

    assert search(users['user0']['token'], 'channel') == { 'messages': [] }

    channel_join(users['user0']['token'], channel_id)

    message2 = message_send(users['admin']['token'], channel_id, 'Now Im in a channel')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'Now Im in a channel',
    }

    searched_messages = search(users['user0']['token'], 'no channels')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info not in popped

def test_other_search_no_messages(initialise_user_data):
    users = initialise_user_data

    assert search(users['user0']['token'], 'There are no messages') == { 'messages': [] }

def test_other_search_empty_query(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    channel_join(users['user0']['token'], channel_id)

    message1 = message_send(users['admin']['token'], channel_id, 'this is message1')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message1',
    }

    message2 = message_send(users['admin']['token'], channel_id, 'this is message2')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message2',
    }

    searched_messages = search(users['user0']['token'], '')
    popped =  pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_other_search_admin(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id = initialise_channel_data['user0_priv']['channel_id']

    message1 = message_send(users['user0']['token'], channel_id, 'private')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['user0']['u_id'],
        'message' : 'private',
    }

    searched_messages = search(users['admin']['token'], 'priv')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped

def test_other_search_multiple_channels(initialise_user_data, initialise_channel_data):
    users = initialise_user_data
    channel_id1 = initialise_channel_data['admin_publ']['channel_id']
    channel_id2 = initialise_channel_data['admin_priv']['channel_id']

    message1 = message_send(users['admin']['token'], channel_id1, 'channel1')
    message1_info = {
        'message_id' : message1['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'channel1',
    }

    message2 = message_send(users['admin']['token'], channel_id2, 'channel2')
    message2_info = {
        'message_id' : message2['message_id'],
        'u_id' : users['admin']['u_id'],
        'message' : 'channel2',
    }

    searched_messages = search(users['admin']['token'], 'channel')
    popped = pop_datetimes(searched_messages['messages'])
    assert message1_info in popped
    assert message2_info in popped

def test_other_search_invalid_token():
    clear()

    invalid_token = ' '

    with pytest.raises(AccessError):
        search(invalid_token, 'This should be illegal')

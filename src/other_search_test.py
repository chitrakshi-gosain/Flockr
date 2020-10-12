from other import clear, search
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

def initialise_data():
    #create users
    #The first user to sign up is global owner
    admin_details = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0_details = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    user1_details = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    #create channels
    channel_publ_details = channels_create(admin_details['token'], "publ0", True)
    channel_priv_details = channels_create(admin_details['token'], "priv0", False)

    channel_priv_user_details = channels_create(user0_details['token'], 'priv1', False)

    return ({ # users
        'admin' : admin_details,
        'user0' : user0_details,
        'user1' : user1_details,
    },
    { # channels
        'publ' : channel_publ_details,
        'priv' : channel_priv_details,
        'user_priv' : channel_priv_user_details,
    })

def pop_datetimes(messages):
    for entry in messages:
        entry.pop('time_created')
    return messages

def test_other_search_not_in_channels():
    clear()
    users, channels = initialise_data()

    message_send(users['admin']['token'], channels['publ']['channel_id'], 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_join_channel():
    clear()
    users, channels = initialise_data()

    message1_id = message_send(users['admin']['token'], channels['publ']['channel_id'], 'I am in no channels')
    message1_info = {
        'message_id' : message1_id,
        'u_id' : users['admin']['u_id'],
        'message' : 'I am in no channels',
    }

    assert search(users['user0']['token'], 'channel') == { 'messages': [] }

    channel_join(users['user0']['token'], channels['publ']['channel_id'])

    message2_id = message_send(users['admin']['token'], channels['publ']['channel_id'], 'Now Im in a channel')
    message2_info = {
        'message_id' : message2_id,
        'u_id' : users['admin']['u_id'],
        'message' : 'Now Im in a channel',
    }

    searched_messages = search(users['user0']['token'], 'channel')
    assert pop_datetimes(searched_messages['messages']) == [message1_info, message2_info]

def test_other_search_no_messages():
    clear()
    users = initialise_data()[0]

    assert search(users['user0']['token'], 'There are no messages') == { 'messages': [] }

def test_other_search_empty_query():
    clear()
    users, channels = initialise_data()

    channel_join(users['user0']['token'], channels['publ']['channel_id'])

    message1_id = message_send(users['admin']['token'], channels['publ']['channel_id'], 'this is message1')
    message1_info = {
        'message_id' : message1_id,
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message1',
    }

    message2_id = message_send(users['admin']['token'], channels['publ']['channel_id'], 'this is message2')
    message2_info = {
        'message_id' : message2_id,
        'u_id' : users['admin']['u_id'],
        'message' : 'this is message2',
    }

    searched_messages = search(users['user0']['token'], '')
    assert pop_datetimes(searched_messages['messages']) == [message1_info, message2_info]

def test_other_search_admin():
    clear()
    users, channels = initialise_data()

    message1_id = message_send(users['user0']['token'], channels['user_priv']['channel_id'], 'private')
    message1_info = {
        'message_id' : message1_id,
        'u_id' : users['user0']['u_id'],
        'message' : 'private',
    }

    searched_messages = search(users['admin']['token'], 'priv')
    assert pop_datetimes(searched_messages['messages']) == [message1_info]

def test_other_search_invalid_token():
    clear()
    users = initialise_data()[0]

    invalid_token = ' '

    with pytest.raises(AccessError):
        search(invalid_token, 'This should be illegal')

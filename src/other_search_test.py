from channel import channel_join
from other import clear, admin_userpermission_change
from auth import auth_register
from channels import channels_create

import pytest
from error import InputError, AccessError

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> intialise_data() return { users }, { channels }
-> test_other_search_()
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
'''

'''
message: [{'message_id':0,
           'u_id' : 0,
           'message' : 'fwidwsadwad',
           'time_created' : datetime
        }]
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

def test_other_search_basic():
    clear()
    users, channels = initialise_data()
    pass

def test_other_search_in_no_channels():
    clear()
    users, channels = initialise_data()

    message_send(users['admin']['token'], channels['publ']['channel_id'], 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_join_channel():
    clear()
    users, channels = initialise_data()

    message_id = message_send(users['admin']['token'], channels['publ']['channel_id'], 'I am in no channels')
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

    channel_join(users['user0']['token'], channels['publ']['channel_id'])
    #We can't get exact channel details
    assert search(users['user0']['token'], 'I am in no channels') == { 'messages': [] }

def test_other_search_no_messages():
    clear()
    users, channels = initialise_data()
    pass

def test_other_search_empty_query():
    clear()
    users, channels = initialise_data()
    pass

def test_other_seach_admin():
    clear()
    users, channels = initialise_data()
    pass

def test_other_seach_invalid_token():
    clear()
    users, channels = initialise_data()
    pass

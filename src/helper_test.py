'''
Created collaboratively by Wed15Team2 2020 T3
Contributers - Jordan Hunyh, Chitrakshi Gosain, Cyrus Wilkie,
               Ahmet Karatas, Joseph Knox

Iteration 1
'''

import unittest
from helper import *
import data
import auth
import channel
import channels
import other

def initialise_data():
    data.data = {
        'users': [
            { # user -> u_id : 0
                'u_id' : 0,
                'is_admin' : True,
                'email' : 'blah0@domain',
                'name_first' : 'fname0',
                'name_last' : 'lname0',
                'handle_str' : 'fname0lname0',
                'token' : 'blah0@domain',
                'password' : 'password0'
            },
            { # user -> u_id : 1
                'u_id' : 1,
                'is_admin' : False,
                'email' : 'blah1@domain',
                'name_first' : 'fname1',
                'name_last' : 'lname1',
                'handle_str' : 'fname1lname1',
                'token' : 'blah1@domain',
                'password' : 'password1'
            }
        ],

        'channels' : [
            { # channels -> channel_id : 0
                'channel_id' : 0,
                'name' : 'ch_name0',
                'is_public' : True,
                'owner_members' : [ # owner_memebers of channel_id : 0
                    {
                        'u_id' : 0,
                        'name_first' : 'fname0',
                        'name_last' : 'fname1',
                    }
                ],
                'all_members' : [ # all_members of channel_id : 0
                    {
                        'u_id' : 0,
                        'name_first' : 'fname0',
                        'name_last' : 'fname0',
                    },
                    {
                        'u_id' : 1,
                        'name_first' : 'fname1',
                        'name_last' : 'fname1',
                    }
                ],
                'messages' : [ # messages of channel_id : 0
                    { # mesages -> message_id : 0
                        'message_id' : 0,
                        'u_id' : 0,
                        'message' : 'messagecontents0',
                        'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    },
                    { # mesages -> message_id : 1
                        'message_id' : 1,
                        'u_id' : 0,
                        'message' : 'messagecontents1',
                        'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    }
                ]
            },
            { # channels -> channel_id : 1
                'channel_id' : 1,
                'name' : 'ch_name1',
                'is_public' : False,
                'owner_members' : [ # owner_memebers of channel_id : 1
                    {
                        'u_id' : 1,
                        'name_first' : 'fname1',
                        'name_last' : 'fname1',
                    }
                ],
                'all_members' : [# all_memebers of channel_id : 1
                    {
                        'u_id' : 0,
                        'name_first' : 'fname0',
                        'name_last' : 'fname0',
                    },
                    {
                        'u_id' : 1,
                        'name_first' : 'fname1',
                        'name_last' : 'fname1',
                    }
                ],
                'messages' : [ # messages of channel_id : 1
                    { # mesages -> message_id : 0
                        'message_id' : 0,
                        'u_id' : 0,
                        'message' : 'messagecontents0',
                        'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    }
                ]
            }
        ]
    }

def test_check_if_valid_email():
    pass

def test_check_if_valid_password():
    pass

def test_check_string_length_and_whitespace():
    # check name_first(1-50 char limit), name_last(1-50 char limit) and
    # handle_str(3-20 char limit), all char limits are inclusive
    pass

def test_invalidating_token():
    pass

def test_get_channel_info():
    other.clear()
    initialise_data()

    assert get_channel_info(-1) == False
    assert get_channel_info(0) == data.data['channels'][0]
    assert get_channel_info(1) == data.data['channels'][1]

def test_is_user_authorised():
    other.clear()
    initialise_data()

    user0 = get_user_info('u_id', 0)
    token0 = user0["token"]
    user1 = get_user_info('u_id', 1)
    token1 = user1["token"]

    assert is_user_authorised(token0, 0)
    assert is_user_authorised(token0, 1)
    assert is_user_authorised(token1, 1)
    assert not is_user_authorised(token1, 0)


def test_is_channel_owner():
    other.clear()
    initialise_data()

    assert is_channel_owner(0, 0)
    assert not is_channel_owner(0, 1)
    assert is_channel_owner(1, 1)
    assert not is_channel_owner(1, 0)

def test_get_user_info():
    other.clear()
    initialise_data()

    assert get_user_info('u_id', -1) == False
    assert get_user_info('token', ' ') == False
    assert get_user_info('email', ' ') == False

    assert get_user_info('u_id', 0) == data.data['users'][0]
    assert get_user_info('token', 'blah1@domain') == data.data['users'][1]
    assert get_user_info('email', 'blah1@domain') == data.data['users'][1]

def test_is_user_in_channel():
    other.clear()
    initialise_data()

    assert is_user_in_channel(0, 0) == True
    assert is_user_in_channel(0, 1) == True
    assert is_user_in_channel(1, 0) == True
    assert is_user_in_channel(1, 1) == True

def test_get_message_info():
    other.clear()
    initialise_data()

    assert get_message_info(0) == {
        'message_id': 0,
        'u_id': 0,
        'message': 'messagecontents0',
        'timecreated': 'datetime(YYYY, MM, DD, HH, MM)'
    }
    assert get_message_info(1) == {
        'message_id': 1,
        'u_id': 0,
        'message': 'messagecontents1',
        'timecreated': 'datetime(YYYY, MM, DD, HH, MM)'
    }
    assert not get_message_info(2)

def test_update_data():
    pass

def test_check_password():
    pass

def test_store_generated_token():
    pass

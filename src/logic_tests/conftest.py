'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Chitrakshi Gosain, Jordan Hunyh, Ahmet Karatas,
               Cyrus Wilkie, Joseph Knox

Iteration 2
'''

import pytest
from auth import auth_register
from channels import channels_create
from other import clear
import data

'''
****************************BASIC TEMPLATE******************************
'''

'''
This file contains all the fixtures used in *test.py
'''

'''
FUNCTIONS_USED_FOR_THIS FIXTURE_FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, firstname, lastname)
-> channels_create(token) return {channel_id}
'''

@pytest.fixture
def reset():
    '''
    Resets the internal data of the application to it's initial state
    '''

    clear()


@pytest.fixture
def initialise_user_data(reset):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    admin_details = auth_register('admin@email.com', 'admin_pass1!', 'admin_first', 'admin_last')

    owner_details = auth_register('owner@email.com', 'owner_pass1!', 'owner_first', 'owner_last')

    user0_details = auth_register('user0@email.com', 'user0_pass1!', 'user0_first', 'user0_last')

    user1_details = auth_register('user1@email.com', 'user1_pass1!', 'user1_first', 'user1_last')

    user2_details = auth_register('user2@email.com', 'user2_pass1!', 'user2_first', 'user2_last')

    user3_details = auth_register('user3@email.com', 'user3_pass1!', 'user3_first', 'user3_last')

    return {
        'admin': admin_details,
        'owner': owner_details,
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details
    }

@pytest.fixture
def initialise_channel_data(initialise_user_data):
    '''
    Creates few channels with descriptive data for testing
    '''

    admin_token = initialise_user_data['admin']['token']
    admin_public_details = channels_create(admin_token, 'admin_public', True)
    admin_private_details = channels_create(admin_token, 'admin_private1', False)

    owner_token = initialise_user_data['owner']['token']
    owner_public_details = channels_create(owner_token, 'owner_public', True)
    owner_private_details = channels_create(owner_token, 'owner_private1', False)

    user_token = initialise_user_data['user0']['token']
    user_public_details = channels_create(user_token, 'private', True)
    user_private_details = channels_create(user_token, 'private', False)

    return {
        'admin_publ': admin_public_details,
        'admin_priv': admin_private_details,
        'owner_publ': owner_public_details,
        'owner_priv': owner_private_details,
        'user0_publ': user_public_details,
        'user0_priv': user_private_details
    }

@pytest.fixture
def initialise_data():
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    data.data = {
        'users': [
            { # user -> u_id : 0
                'u_id' : 0,
                'is_admin' : True,
                'email' : 'blah0@domain',
                'name_first' : 'fname0',
                'name_last' : 'lname0',
                'handle_str' : 'fname0lname0',
                'token' : '0',
                'password' : 'password0'
            },
            { # user -> u_id : 1
                'u_id' : 1,
                'is_admin' : False,
                'email' : 'blah1@domain',
                'name_first' : 'fname1',
                'name_last' : 'lname1',
                'handle_str' : 'fname1lname1',
                'token' : '1',
                'password' : 'password1'
            }
        ],

        'channels' : [
            { # channels -> channel_id : 0
                'channel_id' : 0,
                'name' : 'ch_name0',
                'is_public' : True,
                'owner_members' : [ # owner_members of channel_id : 0
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
                'owner_members' : [ # owner_members of channel_id : 1
                    {
                        'u_id' : 1,
                        'name_first' : 'fname1',
                        'name_last' : 'fname1',
                    }
                ],
                'all_members' : [# all_members of channel_id : 1
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
        ],

        'messages': [
            { # mesages -> message_id : 0
                'message_id' : 0,
                'u_id' : 0,
                'message' : 'messagecontents0',
                'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
            }
        ],

        'valid_tokens': [ # format  => token : u_id
        ]
    }

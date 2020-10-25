'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Chitrakshi Gosain, Joseph Knox, Cyrus Wilkie,
               Jordan Hunyh, Ahmet Karatas

Iteration 1 & 2
'''

'''
****************************BASIC TEMPLATE******************************
'''

'''
This file contains the empty data dictionary which acts as the backend
for our implementation.
'''

'''
Modification log:
25/09: added is_admin key to users' dict and is_public key to channels's dict
01/10: changed data in user['handle_str'], user['token'] and user['password']
       as per the implementation, modified/added comments, also added a header
       comment
02/10: Ensured data dictionary is blank at execution
10/10: added 'messages' and 'valid_token' keys

the global variable data is a listed dictionary
'''

data = {
        'users': [],
        'channels': [],
        'messages': [],
        'valid_tokens': []
        }

'''
data = {
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

    'valid_tokens': { # format  => token : u_id
    }
}
'''

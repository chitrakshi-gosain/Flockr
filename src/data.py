'''
Created collaboratively by Wed15Team2 2020 T3
Used to store data for our Flockr implementation
'''

# Modification log:
# 25/09: added is_admin key to users' dict and is_public key to channels's dict
# 01/10: changed data in user['handle_str'], user['token'] and user['password']
#        as per the implementation, modified/added comments, also added a header
#        comment
# 02/10: Ensured data dictionary is blank at execution
# 10/10: added 'messages' and 'valid_token' keys

# the global variable data is a listed dictionary

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
    
        'fheu' : 0
        'grbehy' : 0 
        'rbjh' : 1 
        'rgbhij' : 1
        # (this will be way more easier to look through)
        # (Ask Hayden or Michael for suggestions.)
    }
    
    # [  
    #     { # valid(active) tokens for user with u_id : 0
    #         'u_id': 0
    #         'tokens': ['fheu', 'grbehy']
    #     },

    #     { # valid(active) tokens for user with u_id : 1
    #         'u_id': 1
    #         'tokens': ['rbjh', 'rgbhij']
    #     }
    # ]
    
}
'''

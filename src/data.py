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

27/10: Added iteration3 stuff:
            standups in channel
            reacts in message,
            reset_codes in data
            profile_pic url in user
the global variable data is a listed dictionary
'''

data = {
        'users': [],
        'channels': [],
        'messages': [],
        'valid_tokens': [],
        'reset_codes': {},
        'password_record': {}
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
            'profile_img_url': '', #local url
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
            'profile_img_url': '', #local url
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
                    'profile_img_url': '',
                }
            ],
            'all_members' : [ # all_members of channel_id : 0
                {
                    'u_id' : 0,
                    'name_first' : 'fname0',
                    'name_last' : 'fname0',
                    'profile_img_url': '',
                },
                {
                    'u_id' : 1,
                    'name_first' : 'fname1',
                    'name_last' : 'fname1',
                    'profile_img_url': '',
                }
            ],
            'messages' : [ # messages of channel_id : 0
                { # mesages -> message_id : 0
                    'message_id' : 0,
                    'u_id' : 0,
                    'message' : 'messagecontents0',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    'is_pinned' : True,
                    'reacts' : {
                        'thumbs_up' : [u_id, 1, 2],
                        'heart' : [u_id, 0] #list of users
                    }
                },
                { # mesages -> message_id : 1
                    'message_id' : 1,
                    'u_id' : 0,
                    'message' : 'messagecontents1',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    'is_pinned' : False,
                    'reacts' : {
                        'thumbs_up' : [u_id, 2],
                        'heart' : [u_id, 1] #list of users
                    }
                }
            ],
            'standup': {
                'u_id': 0,
                'time_start': 1201843272, #unix timestamp
                'time_finish': 1201843572,
                'messages': [
                    {
                        'u_id': 0,
                        'name': 'user0'
                        'message': 'this is standup'
                    },
                    {
                        'u_id': 1,
                        'name': 'user1'
                        'message': 'message2'
                    }
                ] #message_send all as 1 message at end of standup
            }
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
                    'profile_img_url': '',
                }
            ],
            'all_members' : [# all_members of channel_id : 1
                {
                    'u_id' : 0,
                    'name_first' : 'fname0',
                    'name_last' : 'fname0',
                    'profile_img_url': '',
                },
                {
                    'u_id' : 1,
                    'name_first' : 'fname1',
                    'name_last' : 'fname1',
                    'profile_img_url': '',
                }
            ],
            'messages' : [ # messages of channel_id : 1
                { # mesages -> message_id : 0
                    'message_id' : 0,
                    'u_id' : 0,
                    'message' : 'messagecontents0',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                    'is_pinned' : True,
                    'reacts' : {
                        'thumbs_up' : [u_id, 0, 1, 2],
                        'heart' : [u_id] #list of users
                    }
                }
            ],
            'standup': {
                'u_id': 1,
                'time_start': 120238921, #unix timestamp
                'time_finish': 120239921,
                'messages': [
                    {
                        'u_id': 0,
                        'name': 'user0'
                        'message': 'this is standup'
                    },
                    {
                        'u_id': 1,
                        'name': 'user1'
                        'message': 'message2'
                    }
                ] #message_send all as 1 message at end of standup
            }
        }
    ],

    'messages': [
        { # mesages -> message_id : 0
            'message_id' : 0,
            'u_id' : 0,
            'message' : 'messagecontents0',
            'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
            'is_pinned' : True,
            'reacts' : {
                'thumbs_up' : [u_id, 1, 2],
                'heart' : [u_id, 0] #list of users
            }
        }
    ],

    'valid_tokens': { # format  => token : u_id
    },

    'reset_codes': {
        'code1' : email_id,
        'code2' : 'user0@email.com'
    },

    'password_record': {
        'user0@email.com' : {'pass1', 'pass2'},
        'user1@email.com' : {'pass1', 'pass2'}
    }

}
'''

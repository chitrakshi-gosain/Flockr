# can we have comments in coordination, would be easier to relate.

#added admin variable to users
#added is_private to channels

data = {
    'users': [
        { #user -> u_id: 0
            'u_id' : 0,
            'is_admin' : True,
            'email' : 'blah0@domain',
            'name_first' : 'fname0',
            'name_last' : 'lname0',
            'handle_str' : 'handle0'
            'token' : 'fname0' + 'lname0'
            'password' : 'pass0'
        },
        { #user -> u_id: 1
            'u_id' : 1,
            'is_admin' : False,
            'email' : 'blah1@domain',
            'name_first' : 'fname1',
            'name_last' : 'lname1',
            'handle_str' : 'handle1'
            'token' : 'fname1' + 'lname1'
            'password' : 'pass1'
        }
    ],

    'channels' : [
        { #channel0
            'channel_id' : 0,
            'name' : 'ch_name0',
            'is_private' : True,
            'owner_members' : [ #_members
                {
                    'u_id' : 0,
                    'name_first' : 'fname0',
                    'name_last' : 'fname1',
                }
            ],
            'all_members' : [
                {
                    'u_id' : 0,
                    'name_first' : 'fname0',
                    'name_last' : 'fname0',
                },
                {
                    'u_id' : 1,
                    'name_first' : 'fname1',
                    'name_last' : 'fname1',
                },
            ],
            'messages' : [ #messages
                {
                    'message_id' : 0,
                    'u_id' : 0,
                    'message' : 'messagecontents0',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                },
                {
                    'message_id' : 1,
                    'u_id' : 0,
                    'message' : 'messagecontents1',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                },
            ]
        },
        { #channel1
            'channel_id' : 1,
            'name' : 'ch_name1',
            'is_private' : False,
            'owner_members' : [ #_members
                {
                    'u_id' : 1,
                    'name_first' : 'fname1',
                    'name_last' : 'fname1',
                }
            ],
            'all_members' : [
                {
                    'u_id' : 0,
                    'name_first' : 'fname0',
                    'name_last' : 'fname0',
                },
                {
                    'u_id' : 1,
                    'name_first' : 'fname1',
                    'name_last' : 'fname1',
                },
            ],
            'messages' : [ #messages
                {
                    'message_id' : 0,
                    'u_id' : 0,
                    'message' : 'messagecontents0',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)' #(not in quotes)
                },
            ]
        },
    ]
}

data = {
    'users': [
        { #user -> u_id: 0
            'u_id' : 0,
            'email' : 'blah0@domain',
            'name_first' : 'fname0',
            'name_last' : 'lname0',
            'handle_str' : 'handle0'
        },
        { #user -> u_id: 1
            'u_id' : 1,
            'email' : 'blah1@domain',
            'name_first' : 'fname1',
            'name_last' : 'lname1',
            'handle_str' : 'handle1'
        }
    ],

    'channels' : [
        { #channel0
            'channel_id' : 0,
            'name' : 'ch_name0',
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

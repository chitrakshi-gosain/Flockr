import data
from error import AccessError, InputError

# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Cyrus Wilkie

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> channels_list(token) return {channels}
-> channels_listall(token) return {channels}
-> channels_create(token) return {channel_id}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> name: string
    -> is_public: boolean
    -> {channels}: dictionary
    -> {channel_id}: dictionary
'''

def channels_list(token):
    '''
    DESCRIPTION:
    Provide a list of all channels (and
    their associated details) that the
    authorised user is part of

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> AccessError: Invalid token
    '''

    # Checking token validity and finding user that accessed listall
    current_user = {}
    # Loops through users until matching token is found
    for user in data.data['users']:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    # Constructing list of all channels
    channel_list = []

    for channel in data.data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == current_user['u_id']:
                channel_details = {
                    'channel_id': channel['channel_id'],
                    'name': channel['name']
                }

                channel_list.append(channel_details)

    return {
        'channels': channel_list
    }

def channels_listall(token):
    '''
    DESCRIPTION:
    Provide a list of all channels (and
    their associated details)

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> AccessError: Invalid token
    '''

    # Checking token validity and finding user that accessed listall
    current_user = {}
    # Loops through users until matching token is found
    for user in data.data['users']:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    # Constructing list of all channels
    channel_list = []

    for channel in data.data['channels']:
        channel_details = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }

        channel_list.append(channel_details)

    return {
        'channels': channel_list
    }

def channels_create(token, name, is_public):
    '''
    DESCRIPTION:
    Creates a new channel with that name
    that is either a public or private channel

    PARAMETERS:
        -> token
        -> name: Name of channel to be created
        -> is_public: Whether the channel is public

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> InputError when any of:
            - Name is more than 20 characters long
    '''

    # Checking token validity and finding user that created channel
    current_user = {}
    # Loops through users until matching token is found
    for user in data.data['users']:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    # Checking channel name size
    if len(name) > 20:
        raise InputError("Channel Name Too Long")

    # channel_id is set by incrementing from the
    # most recently set channel_id
    channel_id = 0

    if data.data['channels'] != []:
        channel_id = data.data['channels'][-1]['channel_id'] + 1

    # data.py dictionary entry is constructed
    new_channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [
            {
                'u_id': current_user['u_id'],
                'name_first': current_user['name_first'],
                'name_last': current_user['name_last']
            }
        ],
        'all_members': [
            {
                'u_id': current_user['u_id'],
                'name_first': current_user['name_first'],
                'name_last': current_user['name_last']
            }
        ],
        'messages': []
    }

    # Entry is added to data.py
    data.data['channels'].append(new_channel)

    return {
        'channel_id': channel_id,
    }

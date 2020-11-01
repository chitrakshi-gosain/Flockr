'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

Iteration 1
'''

import data
from helper import get_user_info
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
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
    Provide a list of all channels (and their associated details) that
    the authorised user is part of

    PARAMETERS:
        -> token : token of the usr

    RETURN VALUES:
        -> channels : list of channels

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # Checking token validity and finding user that accessed listall
    current_user = get_user_info('token', token)

    # If matching token is not found then AccessError is raised
    if not current_user:
        raise AccessError(description="Token passed in is not a valid token")

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
    Provide a list of all channels (and their associated details)

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> channels : list of channels

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # Checking token validity and finding user that accessed listall
    current_user = get_user_info('token', token)

    # If matching token is not found then AccessError is raised
    if not current_user:
        raise AccessError(description="Token passed in is not a valid token")

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
    Creates a new channel with that name that is either a public or
    private channel

    PARAMETERS:
        -> token
        -> name: Name of channel to be created
        -> is_public: Whether the channel is public

    RETURN VALUES:
        -> channel_id : id of the channel created

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> channel name is more than 20 characters long
    '''

    # Checking token validity and finding user that created channel
    current_user = get_user_info('token', token)

    # If matching token is not found then AccessError is raised
    if not current_user:
        raise AccessError(description="Token passed in is not a valid token")

    # Checking channel name size
    if len(name) > 20:
        raise InputError(description="Channel Name Too Long")

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
                'name_last': current_user['name_last'],
                'profile_img_url': current_user['profile_img_url'],
            }
        ],
        'all_members': [
            {
                'u_id': current_user['u_id'],
                'name_first': current_user['name_first'],
                'name_last': current_user['name_last'],
                'profile_img_url': current_user['profile_img_url'],
            }
        ],
        'messages': [],
        'standup': {}
    }

    # Entry is added to data.py
    data.data['channels'].append(new_channel)

    return {
        'channel_id': channel_id,
    }

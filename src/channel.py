'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Joseph Knox, Ahmet Karatas, Jordan Huynh

Iteration 1
'''

from user import user_profile
from error import InputError
from error import AccessError
from helper import get_channel_info, get_user_info, is_user_in_channel, \
    is_user_authorised, is_channel_owner

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> channel_invite(token, channel_id, u_id) return {}
-> channel_details(token, channel_id) return
   {name, owner_members, all_members}
-> channel_messages(token, channel_id, start) return
   {messages, start, end}
-> channel_leave(token, channel_id) return {}
-> channel_join(token, channel_id) return {}
-> channel_addowner(token, channel_id, u_id) return {}
-> channel_removeowner(token, channel_id, u_id) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> channel_id: integer
    -> u_id: integer
    -> start: integer
    -> name: string
    -> owner_members: list of dictionaries, where each dictionary
                      contains types {u_id, name_first, name_last}
    -> all_members: list of dictionaries, where each dictionary contains
                    types {u_id, name_first, name_last}
    -> name_first: string
    -> name_last: string
'''

def channel_invite(token, channel_id, u_id):
    '''
    DESCRIPTION:
    Invites a user (with user id u_id) to join a channel with ID
    channel_id. Once invited the user is added to the channel
    immediately

    PARAMETERS:
        -> token : token of user who called invite
        -> channel_id : id of the channel
        -> u_id : id of the user who is to be invited

    EXCEPTIONS:
    Error type: InputError
        -> channel_id does not refer to a valid channel
        -> u_id does not refer to a valid user
    Error type: AccessError
        -> token passed in is not a valid token
        -> the authorised user is not already a member of the
            channel
    '''

    #order of checks: invalid token, invalid user, invalid channel_id,
    # invoker not in channel
    invoker_info = get_user_info('token', token)
    if not invoker_info:
        raise AccessError(description='Token passed in is not a valid token')

    user_info = get_user_info('u_id', u_id)
    if not user_info:
        raise InputError('u_id does not refer to a valid user')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel_id does not refer to a valid channel')

    if not is_user_in_channel(invoker_info['u_id'], channel_id) and not\
        invoker_info['is_admin']:
        raise AccessError(description='invoker is not part of the channel')

    user_added = {
        'u_id': user_info['u_id'],
        'name_first': user_info['name_first'],
        'name_last': user_info['name_last'],
        'profile_img_url': user_info['profile_img_url'],
        }

    if not is_user_in_channel(u_id, channel_id):
        channel_info['all_members'].append(user_added)

    return {
    }

def channel_details(token, channel_id):
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns a list of
    dictionaries which contain the channel's name, its owner members and
    all of its members.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel

    RETURN VALUES:
        -> name : name of the channel
        -> owner_members :  all owner members of the channels
        -> all_members: all members of the channels, includes owners too

    EXCEPTIONS:
    Error type: InputError
        -> Channel is not valid
    Error type: AccessError
        -> token passed in is not a valid token
        -> User is not an authorised member of the channel
    '''

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='Channel ID is not a valid channel')

    if not user_info['is_admin'] and not \
        is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError(description='Authorised user is not a member of \
            channel with channel_id')

    return {
        'name': channel_info['name'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members']
    }


def channel_messages(token, channel_id, start):
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns the
    messages from the start message to the start + 50'th message.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel
        -> start: the position to start loading the messages

    RETURN VALUES:
        -> messages : messages in the channel
        -> start : start index of messages returned from channel
        -> end : end index of messages returned from channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel is not valid
        -> If start is greater than the number of messages in the
            channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> User is not an authorised member of the channel
    '''

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token ')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='invalid channel_id')

    if not is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError(description="user is not in channel")

    number_of_messages = len(channel_info['messages'])
    if start > number_of_messages:
        raise InputError(description="no more messages")

    messages = channel_info['messages'][::-1]

    end = start + 50
    output = messages[start:end - 1]
    if number_of_messages - start < 50:
        end = -1
        output = messages[start:]

    return {
        'messages': output,
        'start': start,
        'end': end
    }

def channel_leave(token, channel_id):
    '''
    DESCRIPTION:
    Given a channel ID, the user removed as a member of this channel

    PARAMETERS:
        -> token : token of user who is to leave
        -> channel_id : id of the channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> Authorised user is not a member of channel with channel_id
    '''

    #order of check: invalid token, invalid channel, not in channel
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel_id does not refer to a valid channel')

    user_removed = {
        'u_id': user_info['u_id'],
        'name_first': user_info['name_first'],
        'name_last': user_info['name_last'],
        'profile_img_url': user_info['profile_img_url'],
        }

    if user_removed in channel_info['owner_members']:
        channel_info['owner_members'].remove(user_removed)
    if user_removed in channel_info['all_members']:
        channel_info['all_members'].remove(user_removed)
    else:
        raise AccessError(description='User cannot leave channels they are not part of')

    return {
    }

def channel_join(token, channel_id):
    '''
    DESCRIPTION:
    Given a channel_id of a channel that the
    authorised user can join, adds them to that channel

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> channel_id refers to a channel that is private (when the
            authorised user is not a global owner)
    '''

    # order of checks: invalid token, invalid channel, private channel
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel_id does not refer to a valid channel')


    if not channel_info['is_public'] and not user_info['is_admin']:
        raise AccessError(description="only admins can join private channels")

    user_added = {
        'u_id': user_info['u_id'],
        'name_first': user_info['name_first'],
        'name_last': user_info['name_last'],
        'profile_img_url': user_info['profile_img_url'],
        }

    if not is_user_in_channel(user_info['u_id'], channel_id):
        channel_info['all_members'].append(user_added)

    return {
    }


def channel_addowner(token, channel_id, u_id):
    '''
    DESCRIPTION:
    Make user with user id u_id an owner of the channel
    with channel id channel_id

    PARAMETERS:
        -> token : token for authenticating the user
        -> channel_id : id of channel to be added to
        -> u_id : id of user to be added

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
        -> When user with user id u_id is already an owner of the
            channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user is not an owner of the flockr,
           or an owner of this channel
    '''

    # check if token is not valid
    user_info = get_user_info("token", token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    # check if channel_id is not a valid channel id
    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel_id not valid')

     # check if authorised user (based on token) is admin of the flockr,
     # or owner of the channel
    if not is_user_authorised(token, channel_id):
        raise AccessError(description='authorised user is not flockr admin, or an owner of\
             the channel')

    # check if u_id is in the list of the u_ids of existing owners
    # i.e. if the provided u_id is already an owner
    if is_channel_owner(u_id, channel_id):
        raise InputError(description='u_id is already an owner')

    # extracts first and last names from channel dict
    user_info = user_profile(token, u_id)
    user_info = user_info['user']

    name_first = user_info['name_first']
    name_last = user_info['name_last']
    img_url = user_info['profile_img_url']
    user_dict = {'u_id': u_id, 'name_first': name_first, 'name_last': name_last, 'profile_img_url': img_url,}

    # append the given user to the list of owners
    channel_info['owner_members'].append(user_dict)
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    '''
    DESCRIPTION:
    Make user with user id u_id no longer an owner of the channel
    with channel id channel_id

    PARAMETERS:
        -> token : token for authenticating the user
        -> channel_id : id of channel to be removed from
        -> u_id : id of user to be removed
    
    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
        -> When user with user id u_id is not an owner of the channel
    Error type: AccessError
        -> when the authorised user is not an owner of the flockr,
            or an owner of this channel
    '''

    # check if token is not valid
    user_info = get_user_info("token", token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    # check if channel_id is not a valid channel id
    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel_id not valid')

    # check if authorised user (based on token) is admin of the flockr,
    # or owner of the channel
    if not is_user_authorised(token, channel_id):
        raise AccessError(description='authorised user is not flockr admin, or an owner of\
            the channel')

    # check if u_id is not in the list of the u_ids of existing owners
    # i.e. if the provided u_id is not an owner
    if not is_channel_owner(u_id, channel_id):
        raise InputError(description='u_id is not an owner')

    # remove the given user from the list of owners
    u_info = get_user_info("u_id", u_id)
    user_dict = {'u_id': u_id, 'name_first': u_info['name_first'], 'name_last': u_info['name_last'], 'profile_img_url': u_info['profile_img_url'],}

    channel_info['owner_members'].remove(user_dict)

    return {
    }
# Created collaboratively by Wed15Team2 2020 T3
# Contributers - Joseph Knox, Ahmet Karatas, Jordan Huynh

# Iteration 1

import data
import user
from error import InputError
from error import AccessError
#from helper import is_user_authorised1, is_channel_valid, is_token_valid, get_user_info
import helper

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> channel_invite(token, channel_id, u_id) return {}
-> channel_details(token, channel_id) return {name, owner_members, all_members}
-> channel_messages(token, channel_id, start) return {messages, start, end}
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
    -> owner_members: list of dictionaries, where each dictionary contains types {u_id, name_first, name_last}
    -> all_members: list of dictionaries, where each dictionary contains types {u_id, name_first, name_last}
    -> name_first: string
    -> name_last: string
'''

'''
EXCEPTIONS
    * channel_invite
        Error type: InputError
            -> channel_id does not refer to a valid channel
            -> u_id does not refer to a valid user
        Error type: AccessError
            -> the authorised user is not already a member of the channel
    * channel_details
        Error type: InputError
            -> Channel is not valid
            -> Insufficient parameters given
        Error type: AccessError
            -> token passed in is not a valid token
            -> User is not an authorised member of the channel
    * channel_messages
        Error type: InputError
            -> Insufficient parameters given
            -> Channel is not valid
            -> If start is greater than the number of messages in the channel
        Error type: AccessError
            -> token passed in is not a valid token
            -> User is not an authorised member of the channel
    * channel_leave
        Error type: InputError
            -> Channel ID is not a valid channel
        Error type: AccessError
            -> Authorised user is not a member of channel with channel_id
    * channel_join
        Error type: InputError
            -> Channel ID is not a valid channel
        Error type: AccessError
            -> channel_id refers to a channel that is private (when the authorised user is not a global owner)
    * channel_addowner
        Error type: InputError
            -> Channel ID is not a valid channel
            -> When user with user id u_id is already an owner of the channel
        Error type: AccessError
            -> when the authorised user is not an owner of the flockr, or an owner of this channel
    * channel_removeowner
        Error type: InputError
            -> Channel ID is not a valid channel
            -> When user with user id u_id is not an owner of the channel
        Error type: AccessError
            -> when the authorised user is not an owner of the flockr, or an owner of this channel
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

    RETURN VALUES:
    '''

    #order of checks: invalid token, invalid user, invalid channel_id, invoker not in chnnel
    invoker_info = helper.get_user_info('token', token)
    if not invoker_info:
        raise AccessError('token is invalid')

    user_info = helper.get_user_info('u_id', u_id)
    if not user_info:
        raise InputError('u_id does not refer to a vlid user')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel_id does not refer to a valid channel')

    if not helper.is_user_in_channel(invoker_info['u_id'], channel_id) and not invoker_info['is_admin']:
        raise AccessError('invoker is not part of the channel')

    user_added = { 'u_id': user_info['u_id'], 'name_first': user_info['name_first'],
                   'name_last': user_info['name_last'] }

    if not helper.is_user_in_channel(u_id, channel_id):
        channel_info['all_members'].append(user_added)

    return {
    }

def channel_details(token, channel_id):
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns a list of dictionaries
    which contain the channel's name, its owner members and all of its members.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel

    RETURN VALUES:
    # order of checks: insuficient parameters, token validity, channel validity, user authorisation
    '''

    # Testing for insufficient parameters
    if None in {token, channel_id}:
        raise InputError('Insufficient parameters given')

    # Testing for token validity
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    # Retrieving the u_id from the given token

    # Finding if channel is valid and assigning the current channel to a dictionary
    channel_info = helper.get_channel_info(channel_id)

    if channel_info == False:
        raise InputError('Channel ID is not a valid channel')

    if not user_info['is_admin'] and not helper.is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError('Authorised user is not a member of channel with channel_id')

    # Finding if the user is authorised or not
    # user_authorised = helper.is_user_authorised1(token, u_id, channel_info)
    # if not user_authorised:
    #     raise AccessError('Authorised user is not a member of channel with channel_id')

    # Retrieving the information from the assigned dictionary and returning the new dictionary
    channel_contents = {}
    channel_contents.update({'name': channel_info['name']})
    channel_contents.update({'owner_members': channel_info['owner_members']})
    channel_contents.update({'all_members': channel_info['all_members']})
    return channel_contents


def channel_messages(token, channel_id, start):
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns the messages from
    the start message to the start + 50'th message.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel
        -> start: The position to start loading the messages

    RETURN VALUES:
    # order of checks: insuficient parameters, token validity, channel validity, user authorisation
    '''

    # Testing for insufficient parameters
 # Testing for insufficient parameters
    if None in {token, channel_id}:
        raise InputError('Insufficient parameters given')

    # Testing for token validity
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    # Retrieving the u_id from the given token

    # Finding if channel is valid and assigning the current channel to a dictionary
    channel_info = helper.get_channel_info(channel_id)

    if channel_info == False:
        raise InputError('Channel ID is not a valid channel')

    if not user_info['is_admin'] and not helper.is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError('Authorised user is not a member of channel with channel_id')

    # Finding the number of messages in the channel
    num_message = 0
    for message in (channel_info['messages']):
        num_message += 1

    # Checking if the start input given does not exceed the number of messages in the channel
    if start > num_message:
        raise InputError('Start is greater than the total number of messages in the channel')

    messages_history = {'messages': [], 'start': start, 'end': start + 50}
    # start_index is the index of the dictionary where the messages start loading from.
    # If start = 0, start_index will be the index of the last added dictionary.

    start_index = (num_message - 1) - start
    messages_list = []

    # The goal is to load the message dict's from start_index to (start_index - 50)
    for (loop_index, message) in enumerate(channel_info['messages'][start_index:start_index - 50:-1]):
        messages_list.append(message)
        if (start_index - loop_index == 0):
            messages_history.update({'end': -1})
            break

    if len(channel_info['messages']) == 0:
        messages_history.update({'end': -1})

    else:
        messages_history.update({'messages': messages_list})
    return messages_history

def channel_leave(token, channel_id):
    '''
    DESCRIPTION:
    Given a channel ID, the user removed as a member of this channel

    PARAMETERS:
        -> token : token of user who is to leave
        -> channel_id : id of the channel

    RETURN VALUES:
    '''

    #order of check: invalid token, invalid channel, not in channel
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('token is invalid')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel_id does not refer to a valid channel')

    user_removed = { 'u_id': user_info['u_id'], 'name_first': user_info['name_first'],
                     'name_last': user_info['name_last'] }

    if helper.is_channel_owner(user_info['u_id'], channel_id):
        channel_info['owner_members'].remove(user_removed)
    if helper.is_user_in_channel(user_info['u_id'], channel_id):
        channel_info['all_members'].remove(user_removed)
    else:
        raise AccessError('User cannot leave channels they are not part of')

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

    RETURN VALUES:
    '''

    # order of checks: invalid token, invalid channel, private channel
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('invalid token')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel_id does not refer to a valid channel')


    if not channel_info['is_public'] and not user_info['is_admin']:
        raise AccessError("only admins can join private channels")

    user_added = { 'u_id': user_info['u_id'], 'name_first': user_info['name_first'],
                   'name_last': user_info['name_last'] }

    if not helper.is_user_in_channel(user_info['u_id'], channel_id):
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
    '''

    # check if token is not valid
    user_info = helper.get_user_info("token", token)
    if not user_info:
        raise AccessError('invalid token')

    # check if channel_id is not a valid channel id
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel_id not valid')

     # check if authorised user (based on token) is admin of the flockr, or owner of the channel
    if not helper.is_user_authorised(token, channel_id):
        raise AccessError('authorised user is not flockr admin, or an owner of the channel')

    # check if u_id is in the list of the u_ids of existing owners
    # i.e. if the provided u_id is already an owner
    if helper.is_channel_owner(u_id, channel_id):
        raise InputError('u_id is already an owner')

    # extracts first and last names from channel dict
    user_info = user.user_profile(token, u_id)
    user_info = user_info['user']

    name_first = user_info['name_first']
    name_last = user_info['name_last']
    user_dict = {'u_id': u_id, 'name_first': name_first, 'name_last': name_last}

    # append the given user to the list of owners
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            data.data["channels"][channel_id]["owner_members"].append(user_dict.copy())
            break

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
    '''

    # check if token is not valid
    user_info = helper.get_user_info("token", token)
    if not user_info:
        raise AccessError('invalid token')

    # check if channel_id is not a valid channel id
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel_id not valid')

    # check if authorised user (based on token) is admin of the flockr, or owner of the channel
    if not helper.is_user_authorised(token, channel_id):
        raise AccessError('authorised user is not flockr admin, or an owner of the channel')

    # check if u_id is not in the list of the u_ids of existing owners
    # i.e. if the provided u_id is not an owner
    if not helper.is_channel_owner(u_id, channel_id):
        raise InputError('u_id is not an owner')

    # remove the given user from the list of owners
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for i in range(len(channel["owner_members"])):
                if channel["owner_members"][i]["u_id"] == u_id:
                    del data.data["channels"][channel_id]["owner_members"][i]
                    break

    return {
    }

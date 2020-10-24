'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas, Joseph Knox

Iteration 1
'''

from datetime import datetime, timezone
import helper
import data
from error import InputError, AccessError

def message_send(token, channel_id, message):
    '''
    checks that the user if authorised in the channel and sends the message
    '''

    if None in {token, channel_id, message}:
        raise InputError('Insufficient parameters given')

    # Testing for token validity
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    # Retrieving the u_id from the given token
    # Finding if channel is valid and assigning the current channel to a
    # dictionary
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('Channel ID is not a valid channel')

    if not user_info['is_admin'] and not helper.is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError('Authorised user is not a member of channel with channel_id')

    message_id = len(data.data['messages'])

    date = datetime.now()
    time_created = date.replace(tzinfo=timezone.utc).timestamp()

    message_dict = {
        'message_id': message_id,
        'u_id': user_info['u_id'],
        'message': message,
        'time_created': time_created
    }

    data.data['messages'].append(message_dict)
    channel_info['messages'].append(message_dict)

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    '''
    ADD DOCSTRING HERE
    '''

    if None in {token, message_id}:
        raise InputError("Insufficient parameters given")

    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    message_info = helper.get_message_info(message_id)
    if not message_info:
        raise InputError('message_id does not correlate to an existing message_id')

    for channel in data.data['channels']:
        if message_info in channel['messages']:
            channel_info = channel
            break

    #if not admin or not owner or not sender, denied
    if not helper.is_user_authorised(token, channel_info['channel_id']) and not message_info['u_id'] == user_info['u_id']:
        raise AccessError('User is does not have rights to remove message')

    channel_info['messages'].remove(message_info)

    return {
    }

def message_edit(token, message_id, message):
    '''
    DESCRIPTION:
    Given a token, a message_id, and a message,
    finds the sent message with the provided message_id
    and updates its text with the given message.

    PARAMETERS:
        -> token : token of user who called the function
        -> message_id : identification number for intended message to be updated
        -> message : updated text

    RETURN VALUES:
    '''

    # check if token is valid
    user_info = helper.get_user_info("token", token)
    if not user_info:
        raise AccessError('invalid token')

    channel_id = -1
    for channel in data.data['channels']:
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                channel_id = channel["channel_id"]

    # check if message with message_id was sent by the authorised user
    message_info = helper.get_message_info(message_id)
    if user_info["u_id"] != message_info["u_id"] and not \
        helper.is_user_authorised(token, channel_id):
        raise AccessError("message not sent by user, or user is not authorised")

    channel_index = 0
    for channel in data.data['channels']:
        message_index = 0
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                if message == "":
                    del data.data['channels'][channel_index]['messages']\
                        [message_index]
                else:
                    data.data['channels'][channel_index]['messages']\
                        [message_index]['message'] = message
                break
            message_index += 1
        channel_index += 1

    return {
    }

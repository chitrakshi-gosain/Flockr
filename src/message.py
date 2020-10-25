'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas, Joseph Knox

Iteration 1
'''

from datetime import datetime, timezone
from helper import get_user_info, get_channel_info, is_user_in_channel, \
    get_message_info, is_user_authorised
import data
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> message_send(token, channel_id, message) return {message_id}
-> message_remove(token, message_id) return {}
-> message_edit(token, message_id, message) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> channel_id: integer
    -> message_id: integer
    -> message: string
'''

def message_send(token, channel_id, message):
    '''
    DESCRIPTION:
    checks that the user if authorised in
    the channel and sends the message

    PARAMETERS:
        -> token
        -> channel_id : id of channel to send message
        -> message : message contents

    RETURN VALUES:
        -> message_id : id of the sent message

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user has not joined the channel they are
           trying to post to
    Error type: InputError
        -> message is more than 1000 characters 
    '''

    # Testing for token validity
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Invalid Token')

    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='Channel ID is not a valid channel')

    if not user_info['is_admin'] and not is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError(description='Authorised user is not a member of channel with channel_id')

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
    DESCRIPTION:
    Given a message_id for a message, this message is removed from the
    channel

    PARAMETERS:
        -> token
        -> message_id : id of the message to be removed

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> message with message_id was sent by the authorised user
           making this request
        -> the authorised user is an owner of this channel or the flockr
    Error type: InputError
        -> message (based on ID) no longer exists
    '''

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Invalid Token')

    message_info = get_message_info(message_id)
    if not message_info:
        raise InputError(description='message_id does not correlate to an existing message_id')

    for channel in data.data['channels']:
        if message_info in channel['messages']:
            channel_info = channel
            break

    #if not admin or not owner or not sender, denied
    if not is_user_authorised(token, channel_info['channel_id']) and \
    not message_info['u_id'] == user_info['u_id']:
        raise AccessError(description='User is does not have rights to remove message')

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
        -> message_id : identification number for intended message to be
        updated
        -> message : updated text

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> message with message_id was sent by the authorised user
        making this request
        -> the authorised user is an owner of this channel or the flockr
    '''

    # check if token is valid
    user_info = get_user_info("token", token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    channel_id = -1
    for channel in data.data['channels']:
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                channel_id = channel["channel_id"]

    # check if message with message_id was sent by the authorised user
    message_info = get_message_info(message_id)
    if user_info["u_id"] != message_info["u_id"] and not \
        is_user_authorised(token, channel_id):
        raise AccessError(description="message not sent by user, or user is not authorised")

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

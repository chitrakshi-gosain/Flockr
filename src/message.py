# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox, Ahmet Karatas

# Iteration 2

from datetime import datetime
import pytest
import auth
import helper
import data
from channel import channel_join
from channels import channels_create
from error import AccessError, InputError
from other import clear

'''
*********************************BASIC TEMPLATE*********************************
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
    -> message: string
    -> message_id: integer
'''

'''
EXCEPTIONS
    * message_send

    * message_remove
    
    * message_edit
        Error type: AccessError
            -> token passed in is not a valid token
            -> authorised user is not an admin of the flockr or owner of the channel
            -> Message with message_id was not sent by the authorised user making this request
'''


def message_send(token, channel_id, message):
    '''
    checks that the user if authorised in the channel and sends the message
    '''

    if None in [token, channel_id, message]:
        raise InputError('Insufficient parameters given')

    # Testing for token validity
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    # Retrieving the u_id from the given token
    # Finding if channel is valid and assigning the current channel to a dictionary
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('Channel ID is not a valid channel')

    if not user_info['is_admin'] and not helper.is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError('Authorised user is not a member of channel with channel_id')

    message_id = 0

    data.data['messages'] = []
    if data.data['messages'] != []:
        message_id = data.data['messages'][-1]['message_id'] + 1

    date = datetime.now()
    Y = int(datetime.strftime(date, "%Y"))
    m = int(datetime.strftime(date, "%m"))
    d = int(datetime.strftime(date, "%d"))
    H = int(datetime.strftime(date, "%H"))
    M = int(datetime.strftime(date, "%M"))
    S = int(datetime.strftime(date, "%S"))
    timecreated = datetime(Y, m, d, H, M, S)

    message_dict = {
        'message_id': message_id,
        'u_id': user_info['u_id'],
        'message': message,
        'timecreated': timecreated
    }

    data.data['messages'].append(message_dict)

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(message_dict)

    return {
        'message_id': message_id,
    }



def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    '''
    DESCRIPTION:
    Given a token, a message_id, and a message,
    finds the sent message with the provided message_id
    and updates its text with the given message.
    If the given message is an empty string, delete the message.

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

    # check if message with message_id was sent by the authorised user
    message_info = helper.get_message_info(message_id)
    if user_info["u_id"] != message_info["u_id"]:
        raise AccessError("message not sent by user")

    # get channel_id for channel in which the message with message_id was sent
    channel_id = -1
    for channel in data.data['channels']:
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                channel_id = channel["channel_id"]

    # check if authorised user (based on token) is admin of the flockr, or owner of the channel
    if not (user_info["is_admin"] or helper.is_channel_owner(user_info["u_id"], channel_id)):
        raise AccessError('authorised user is not an admin of the flockr,'
                          + ' or an owner of the channel')

    c_index = 0
    for channel in data.data['channels']:
        m_index = 0
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                if message == "":
                    del data.data['channels'][c_index]['messages'][m_index]
                else:
                    data.data['channels'][c_index]['messages'][m_index]['message'] = message
                break
            m_index += 1
        c_index += 1

    return {
    }

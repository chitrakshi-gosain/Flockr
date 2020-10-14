# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 2

import pytest
import auth
import helper
import data
from channel import channel_join
from channels import channels_create
from error import AccessError
from other import clear

def message_send(token, channel_id, message):
    return {
        'message_id': 1,
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

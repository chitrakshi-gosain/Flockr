'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas, Joseph Knox

Iteration 1 & 3
'''

from datetime import datetime, timezone
from helper import get_user_info, get_channel_info, is_user_in_channel, \
    get_message_info, is_user_authorised, post_message_to_channel
import data
import threading
from error import InputError, AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> message_send(token, channel_id, message) return {message_id}
-> message_remove(token, message_id) return {}
-> message_edit(token, message_id, message) return {}
-> message_sendlater(token, channel_id, message, time_sent) return
   {message_id}
-> message_react(token, message_id, react_id) return {}
-> message_unreact(token, message_id, react_id) return {}
-> message_pin(token, message_id) return {}
-> message_unpin(token, message_id) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> channel_id: integer
    -> message_id: integer
    -> message: string
    -> time_sent: int
    -> react_id: int
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

    date = datetime.now(timezone.utc)
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

def message_sendlater(token, channel_id, message, time_sent):
    '''
    DESCRIPTION:
    Send a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future

    PARAMETERS:
        -> token : token of the authenticated user
        -> channel_id : id of channel to send message
        -> message : message contents
        -> time_sent : time in future to send the message at

    RETURN VALUES:
        -> message_id : id of the message which will be sent later
    
    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user has not joined the channel they are
        trying to post to
    Error type : InputError
        -> channel ID is not a valid channel
        -> message is more than 1000 characters
        -> time sent is a time in the past
    '''
    # Checking token
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Invalid Token')

    # Checking channel
    channel_info = get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='Channel ID is not a valid channel')

    # Checking user is a member of channel
    if not user_info['is_admin'] and not is_user_in_channel(user_info['u_id'], channel_id):
        raise AccessError(description='Authorised user is not a member of channel with channel_id')

    # Checking message length
    if len(message) > 1000:
        raise InputError(description='Message is larger than 1000 characters')

    # Checking time_sent
    curr_time = datetime.now(timezone.utc)
    if curr_time.replace(tzinfo=timezone.utc).timestamp() > time_sent:
        raise InputError(description=f'Invalid time {time_sent} {curr_time.replace(tzinfo=timezone.utc).timestamp()}')

    # Constructing message
    message_id = len(data.data['messages'])

    message_dict = {
        'message_id': message_id,
        'u_id': user_info['u_id'],
        'message': message,
        'time_created': time_sent,
    }

    # Sending message
    data.data['messages'].append(message_dict)
    timer_duration = time_sent - curr_time.replace(tzinfo=timezone.utc).timestamp()
    timer = threading.Timer(timer_duration, post_message_to_channel, [message_dict, channel_id])
    timer.start()

    return {
        'message_id': message_id,
    }

def message_react(token, message_id, react_id):
    '''
    DESCRIPTION:
    Given a message within a channel the authorised user is part of, add
    a "react" to that particular message

    PARAMETERS:
        -> token : token of the authenticated user
        -> message_id : id of the message to be reacted
        -> react_id : id of the react, presently only possibility is 1
                      for thumbs up
    
    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> message_id is not a valid message within a channel that the
           authorised user has joined
        -> react_id is not a valid React ID. The only valid react ID the
            frontend has is 1
        -> Message with ID message_id already contains an active React
           with ID react_id from the authorised user
    '''

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
    }

def message_unreact(token, message_id, react_id):
    '''
    DESCRIPTION:
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message

    PARAMETERS:
        -> token : token of the authenticated user
        -> message_id : id of the message to be unreacted
        -> react_id : id of the react, presently only possibility is 1
                      for thumbs up

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> message_id is not a valid message within a channel that the
           authorised user has joined
        -> react_id is not a valid React ID
        -> message with ID message_id does not contain an active React
           with ID react_id
    '''

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
    }

def message_pin(token, message_id):
    '''
    DESCRIPTION:
    Given a message within a channel, mark it as "pinned" to be given
    special display treatment by the frontend

    PARAMETERS:
        -> token : token of the authenticated user
        -> message_id : id of the message to be pinned
    
    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> the authorised user is not a member of the channel that the
           message is within
        -> the authorised user is not an owner
    Error type: InputError
        -> message_id is not a valid message
        -> message with ID message_id is already pinned
    '''

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no InputError(s), hence proceeding forward:

    return {
    }

def message_unpin(token, message_id):
    '''
    DESCRIPTION:
    Given a message within a channel, remove it's mark as unpinned

    PARAMETERS:
        -> token : token of the authenticated user
        -> message_id : id of the message to be unpinned
    
    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> message_id is not a valid message
        -> message with ID message_id is already unpinned
    Error type: InputError
        -> the authorised user is not a member of the channel that the
           message is within
        -> the authorised user is not an owner
    '''

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
    }

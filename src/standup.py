'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - NAMES HERE

Iteration 3
'''

from error import InputError, AccessError
import helper
from datetime import datetime, timezone
import data

import threading
import time
'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> standup_start(token, channel_id, length) return {time_finish}
-> standup_active(token,channel_id) return {is_active, time_finish}
-> standup_send(token, channel_id, message) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> channel_id: int
    -> length: int
    -> time_finish: int
    -> is_active: boolean
    -> message: string
'''

'''
KEEP IN MIND:

************************SECTION 6.9 of Readme.md************************

Once standups are finished, all of the messages sent to standup/send are
packaged together in one single message posted by the user who started
the standup and sent as a message to the channel the standup was started
in, timestamped at the moment the standup finished.

The structure of the packaged message is like this:

For example:

+----------------------------------------------------------------------+
+ hayden: I ate a catfish                                              +
+ rob: I went to kmart                                                 +
+ michelle: I ate a toaster                                            +
+ isaac: my catfish ate a toaster                                      +
+----------------------------------------------------------------------+

Standups can be started on the frontend by typing "/standup X", where X
is the number of seconds that the standup lasts for, into the message
input and clicking send.
'''

def standup_start(token, channel_id, length):
    '''
    DESCRIPTION:
    For a given channel, start the standup period whereby for the next
    "length" seconds if someone calls "standup_send" with a message, it
    is buffered during the X second window then at the end of the X
    second window a message will be added to the message queue in the
    channel from the user who started the standup. X is an integer that
    denotes the number of seconds that the standup occurs for

    PARAMETERS:
        -> token : token of the authenticated user
        -> channel_id : id of the channel to start standup in
        -> length : length of period standup should last for

    RETURN VALUES:
        -> time_finish : the time when standup will end in the
                         particular channel

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> channel ID is not a valid channel
        -> an active standup is currently running in this channel
    '''

    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('invalid token')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('invalid channel id')

    if channel_info['standup'] != {}:
        raise InputError('standup already exists')

    now = int(datetime.now(timezone.utc).timestamp())

    channel_info['standup'] = {
        'u_id': user_info['u_id'],
        'time_start': now,
        'time_finish': now+length,
        'messages': []
    }

    t = threading.Timer(length, standup_end, [channel_id])
    t.start()

    return {
        'time_finish': now+length
        }

def standup_active(token,channel_id):
    '''
    DESCRIPTION:
    For a given channel, return whether a standup is active in it, and
    what time the standup finishes. If no standup is active, then
    time_finish returns None

    PARAMETERS:
        -> token : token of the authenticated user
        -> channel_id : id of the channel to check where standup is
                        running

    RETURN VALUES:
        -> is_active : status of standup in particular channel
        -> time_finish : the time when standup will end in the
                         particular channel

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> channel ID is not a valid channel
    '''
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('invalid token')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('invalid channel id')

    if channel_info['standup'] == {}: #standup does not currently exist
        is_active = False
        time_finish = None

    else:
        is_active = True
        time_finish = channel_info['standup']['time_finish']

    return {
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    '''
    DESCRIPTION:
    Sending a message to get buffered in the standup queue, assuming a
    standup is currently active

    PARAMETERS:
        -> token : token of the authenticated user
        -> channel_id : id of the channel to send message in for standup

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> the authorised user is not a member of the channel that the
           message is within
    Error type: InputError
        -> channel ID is not a valid channel
        -> message is more than 1000 characters
        -> an active standup is not currently running in this channel
    '''

    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('invalid token')

    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('invalid channel id')

    if not helper.is_user_in_channel(user_info['u_id'], channel_info['channel_id']):
        raise AccessError('user is not in channel')

    if not standup_active(token, channel_id)['is_active']:
        raise InputError('there is no active standup in channel')

    if not (1 <= len(message) <= 1000):
        raise InputError('messages cannot be 0 or more than 1000 characters')

    user_message = f"{user_info['name_first']}: {message}"
    channel_info['standup']['messages'].append(user_message)

    return {
    }

def standup_end(channel_id):
    '''
    reset the channel's standup state and send message
    '''

    channel_info = helper.get_channel_info(channel_id)
    #collect and send messages
    if channel_info: #nested if statements to prevent bool subscript errors
        if channel_info['standup'] != {}:
            if channel_info['standup']['messages']:
                message_out = '\n'.join(channel_info['standup']['messages'])
                message_id = len(data.data['messages'])

                message_dict = {
                    'message_id': message_id,
                    'u_id': channel_info['standup']['u_id'],
                    'message': message_out,
                    'time_created': channel_info['standup']['time_finish'],
                    'reacts': [
                        {'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}
                    ],
                    'is_pinned': False
                }
                data.data['messages'].append(message_dict)
                channel_info['messages'].append(message_dict)

        channel_info['standup'] = {}

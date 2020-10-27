'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - NAMES HERE

Iteration 3
'''

from error import InputError, AccessError
from helper import get_user_info

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

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
        'time_finish': 0
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

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
        'is_active': True,
        'time_finish': 0
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

    # Checking for AccessError:

    # Checking for InputError(s):

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    return {
    }
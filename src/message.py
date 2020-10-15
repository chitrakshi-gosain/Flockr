from datetime import datetime
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
    # Finding if channel is valid and assigning the current channel to a dictionary
    channel_info = helper.get_channel_info(channel_id)
    if channel_info == False:
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
    '''
    checks that the user if authorised in the channel and deletes the message
    '''
    
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
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

    messages_list_created = False
    for group in data.data:
        if group == 'messages':
            messages_list_created = True

    if messages_list_created:
        message_id = data.data['messages'][-1]['message_id'] + 1

    else:
        data.data['messages'] = []    
        message_id = 0
    

    date = datetime.now()
    Y = int(datetime.strftime(date, "%Y"))
    m = int(datetime.strftime(date, "%m"))
    d = int(datetime.strftime(date, "%d"))
    H = int(datetime.strftime(date, "%H"))
    M = int(datetime.strftime(date, "%M"))
    S = int(datetime.strftime(date, "%S"))
    time_created = datetime(Y, m, d, H, M, S)
    
    message_dict = {
        'message_id': message_id,
        'u_id': user_info['u_id'],
        'message': message,
        'time_created': time_created
    } 

    data.data['messages'].append(message_dict)

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(message_dict)
    
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):

    # Testing for insufficient parameters
    if None in {token, message_id}:
        raise InputError("Insufficient parameters given")

    # Testing to see if the message exists
    message_exists = False
    for channel in data.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_exists = True
                channel_info = channel
                message_info = message
                break


    if not message_exists:
        raise InputError('message_id does not correlate to an existing message_id')

    # Testing for token validity
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('Invalid Token')

    # if the user did not send the message

    if message_info['u_id'] != user_info['u_id']:
        # if the user is not an owner of the channel
        for owner in channel_info['owner_members']:
            if owner['u_id'] != user_info['u_id']:
                raise AccessError('User has neither sent the message, now is an owner of the channel')

    for (i, message) in enumerate(channel_info['messages']):
        if message['message_id'] == message_id:
            del channel_info['messages'][i]

    return {
    }

# def message_edit(token, message_id, message):
#     return {
#     }
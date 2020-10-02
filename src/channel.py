import data
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    return {
    }

    
def channel_details(token, channel_id):

    is_token_valid(token)
    u_id = find_user_id(token)
    is_user_authorised(token, u_id)
    channel_dict = is_channel_valid(channel_id)

    channel_contents = {}
    channel_contents.update({'name': channel_dict['name']})
    channel_contents.update({'owner_members': channel_dict['owner_members']})
    channel_contents.update({'all_members': channel_dict['all_members']})
    return channel_contents

def channel_messages(token, channel_id, start):

    is_token_valid(token)
    u_id = find_user_id(token)
    is_user_authorised(token, u_id)
    channel_dict = is_channel_valid(channel_id)

    num_message = 0
    for message in (channel_dict['messages']):
        num_message += 1

    if start > num_message:
        raise InputError('Start is greater than the total number of messages in the channel')

    messages_history = {'messages': [], 'start': start, 'end': start + 50}

    # start_index is the index of the dictionary where the messages start loading from.
    # If start = 0, start_index will be the index of the last added dictionary.
    start_index = (num_message - 1) - start       
    messages_list = []                                     

    # The goal is to load messages from the start_index to (start_index -50)    
    for (loop_index, message) in enumerate(channel_dict['messages'][start_index:start_index - 50:-1]):
        messages_list.append(message)
        if (start_index - loop_index == 0):
            messages_history.update({'end': -1})
            break

    messages_history.update({'messages': messages_list})
    return messages_history

def find_user_id(token):                    
    for user in data.data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            return u_id


def is_token_valid(token):
    valid_token = False
    for user in data.data['users']:
        if user['token'] == token:
            valid_token = True

    if not valid_token:                                                 # this wasn't raised in the spec but I think it's something to account for
        raise AccessError['Invalid Token']

def is_user_authorised(token, u_id):
    u_id = find_user_id(token)

    for channel in data.data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                user_authorised = True

    if not user_authorised:
        raise AccessError('Authorised user is not a member of channel with channel_id')

def is_channel_valid(channel_id):

    channel_dict = {}
    channel_valid = False
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel_valid == True
            channel_dict = channel
            break
            
    if not channel_valid:
        raise InputError('Channel ID is not a valid channel')

    return channel_dict

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }

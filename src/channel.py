import data
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    #order of checks: invalid token, invalid user, invalid channel_id, invoker not in chnnel

    is_valid_user = False

    is_valid_invoker = False
    is_invoker_admin = False
    for user in data.data['users']: #check if token is valid -> get user info
        if user['u_id'] == u_id:
            is_valid_user = True
            user_info = {'u_id': user['u_id'], 'name_first': user['name_first'], 'name_last': user['name_last']}

        if user['token'] == token:
            is_valid_invoker = True
            is_invoker_admin = user['is_admin']
            invoker_info = {'u_id': user['u_id'], 'name_first': user['name_first'], 'name_last': user['name_last']}

        if is_valid_invoker and is_valid_user:
            break # stop scanning through unnecessary entries

    if not is_valid_invoker:
        raise AccessError('token is invalid')

    if not is_valid_user:
        raise InputError('u_id does not refer to a valid user')

    is_valid_channel = False
    channel_idx = 0
    for channel in data.data['channels']: #check if channel is valid -> get channel info
        if channel['channel_id'] == channel_id:
            is_valid_channel = True
            is_public = channel['is_public']
            break
        channel_idx += 1

    if not is_valid_channel:
        raise InputError('channel_id does not refer to a valid channel')

    if not is_invoker_admin and not invoker_info in data.data['channels'][channel_idx]['all_members']:
        raise AccessError('invoker is not part of the channel')

    #add valid users to valid channel
    if is_valid_invoker and is_valid_user and is_valid_channel:
        if not user_info in data.data['channels'][channel_idx]['all_members']:
            data.data['channels'][channel_idx]['all_members'].append(user_info)
        else:
            #assume function was not called (to prevent data duplication)
            pass

    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    #order of check: invalid token, invalid channel, not in channel

    is_valid_user = False
    for user in data.data['users']: #check if token is valid -> get user info
        if user['token'] == token:
            is_valid_user = True
            user_info = {'u_id': user['u_id'], 'name_first': user['name_first'], 'name_last': user['name_last']}
            break

    if not is_valid_user:
        raise AccessError('token is invalid')

    is_valid_channel = False
    channel_idx = 0
    for channel in data.data['channels']: #check if channel is valid -> get channel info
        if channel['channel_id'] == channel_id:
            is_valid_channel = True
            break
        channel_idx += 1

    if not is_valid_channel:
        raise InputError('channel_id does not refer to a valid channel')

    #remove valid user from valid channel
    if is_valid_user and is_valid_channel:
        if user_info in data.data['channels'][channel_idx]['all_members']:
            data.data['channels'][channel_idx]['all_members'].remove(user_info)
        else:
            raise AccessError("User cannot leave channels they are not part of")

    return {
    }

def channel_join(token, channel_id):
    # order of checks: invalid token, invalid channel, private channel

    is_valid_user = False
    for user in data.data['users']: #check if token is valid -> get user info
        if user['token'] == token:
            is_valid_user = True
            is_admin = user['is_admin']
            user_info = {'u_id': user['u_id'], 'name_first': user['name_first'], 'name_last': user['name_last']}
            break

    if not is_valid_user:
        raise AccessError('token is invalid')

    is_valid_channel = False
    channel_idx = 0
    for channel in data.data['channels']: #check if channel is valid -> get channel info
        if channel['channel_id'] == channel_id:
            is_valid_channel = True
            is_public = channel['is_public']
            break
        channel_idx += 1

    if not is_valid_channel:
        raise InputError('channel_id does not refer to a valid channel')

    if not is_admin and not is_public:
        raise AccessError('only admins can join private channels')

    #add valid users to valid channel
    if is_valid_user and is_valid_channel:
        if not user_info in data.data['channels'][channel_idx]['all_members']:
            data.data['channels'][channel_idx]['all_members'].append(user_info)
        else:
            #assume function was not called to not create duplicate data
            pass

    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }

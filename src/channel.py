# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox, Ahmet Karatas, Jordan Huynh

# Iteration 1

import data
import user
from error import InputError
from error import AccessError

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

    if None in {token, channel_id}:
        raise InputError('Insufficient parameters given')

    is_token_valid(token)
    u_id = find_user_id(token)
    channel_dict = is_channel_valid(channel_id)
    is_user_authorised(token, u_id, channel_dict)

    channel_contents = {}
    channel_contents.update({'name': channel_dict['name']})
    channel_contents.update({'owner_members': channel_dict['owner_members']})
    channel_contents.update({'all_members': channel_dict['all_members']})
    return channel_contents


def channel_messages(token, channel_id, start):
    if None in {token, channel_id, start}:
        raise InputError('Insufficient parameters given')

    is_token_valid(token)
    u_id = find_user_id(token)
    channel_dict = is_channel_valid(channel_id)
    is_user_authorised(token, u_id, channel_dict)

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

    if len(channel_dict['messages']) == 0:
        messages_history.update({'end': -1})

    else:
        messages_history.update({'messages': messages_list})
    return messages_history

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
        if user_info in data.data['channels'][channel_idx]['owner_members']:
            data.data['channels'][channel_idx]['owner_members'].remove(user_info)
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
    # check if token is not valid
    if token not in [user["token"] for user in data.data["users"]]:
        raise AccessError('invalid token')
    
    # check if authorised user (based on token) is admin of the flockr
    for u in data.data["users"]:
        if token == u["token"] and u["is_admin"] == False:
            raise AccessError('authorised user is not an admin of the flockr')

    # check if authorised user is owner of the channel
    token_uid = find_user_id(token)
    if not is_channel_owner(token_uid, channel_id):
        raise AccessError('authorised user is not an owner of the channel')

    # check if channel_id is not a valid channel id
    if channel_id not in [channel['channel_id'] for channel in data.data['channels']]:
        raise InputError('channel_id not valid')
    
    # searches through data and finds the channel dictionary with the provided channel_id
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel_from_id = channel
            break

    # check if u_id is in the list of the u_ids of existing owners
    # i.e. if the provided u_id is already an owner
    if u_id in [owner['u_id'] for owner in channel_from_id['owner_members']]:
        raise InputError('u_id is already an owner')

    # extracts first and last names from channel dict
    user_info = user.user_profile(token, u_id)
    user_info = user_info['user']
    name_first = user_info['name_first']
    name_last = user_info['name_last']
    user_dict = {'u_id': u_id, 'name_first': name_first, 'name_last': name_last}

    # append the given user to the list of owners
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
                data.data["channels"][channel_id]["owner_members"].append(user_dict.copy())
                break
    
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    # check if token is not valid
    if token not in [user["token"] for user in data.data["users"]]:
        raise AccessError('invalid token')

    # check if authorised user (based on token) is admin of the flockr
    for u in data.data["users"]:
        if token == u["token"] and u["is_admin"] == False:
            raise AccessError('authorised user is not an owner of the flockr')

    # check if authorised user is owner of the channel
    token_uid = find_user_id(token)
    if not is_channel_owner(token_uid, channel_id):
        raise AccessError('authorised user is not an owner of the channel')

    # check if channel_id is not a valid channel id
    if channel_id not in [channel['channel_id'] for channel in data.data['channels']]:
        raise InputError('channel_id not valid')

    # searches through data and finds the channel dictionary with the provided channel_id
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel_from_id = channel
            break

    # check if u_id is not in the list of the u_ids of existing owners
    # i.e. if the provided u_id is not an owner
    if u_id not in [owner['u_id'] for owner in channel_from_id['owner_members']]:
        raise InputError('u_id is not an owner')

    # remove the given user from the list of owners
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for i in range(len(channel["owner_members"])):
                if channel["owner_members"][i]["u_id"] == u_id:
                    del data.data["channels"][channel_id]["owner_members"][i]
                    break

    return {
    }


################ HELPER FUNCTIONS
def is_token_valid(token):
    valid_token = False
    for user in data.data['users']:
        if user['token'] == token:
            valid_token = True

    if not valid_token:
        raise AccessError('Invalid Token')

def find_user_id(token):
    for user in data.data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            return u_id

def is_channel_valid(channel_id):

    channel_dict = {}
    channel_valid = False
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel_valid = True
            channel_dict = channel
            break

    if not channel_valid:
        raise InputError('Channel_id is not valid')

    return channel_dict

def is_user_authorised(token, u_id, channel_dict):
    u_id = find_user_id(token)

    user_authorised = False
    for user in data.data['users']:
        if user['token'] == token:
            user_authorised = user['is_admin']

    for member in channel_dict['all_members']:
        if member['u_id'] == u_id:
            user_authorised = True

    if not user_authorised:
        raise AccessError('Authorised user is not a member of channel with channel_id')

    return user_authorised

def is_channel_owner(u_id, channel_id):
    for channel in data.data['channels']:
        if channel["channel_id"] == channel_id and u_id in [owner["u_id"] for owner in channel["owner_members"]]:
            return True
    return False

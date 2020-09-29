import data

def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    # Checking token validity and finding user that accessed listall
    current_user = {}
    # Loops through users until matching token is found
    for user in users:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    # Constructing list of all channels

    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    # Checking token validity and finding user that created channel
    current_user = {}
    # Loops through users until matching token is found
    for user in users:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    # Checking channel name size
    if len(name) > 20:
        raise InputError("Channel Name Too Long")

    # channel_id is set by incrementing from the
    # most recently set channel_id
    channel_id = 0

    if channels != []:
        channel_id = channels[-1]['channel_id'] + 1

    # data.py dictionary entry is constructed
    new_channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [
            {
                'u_id': current_user['u_id'],
                'name_first': current_user['name_first'],
                'name_last': current_user['name_last']
            }
        ],
        'all_members': [
            {
                'u_id': current_user['u_id'],
                'name_first': current_user['name_first'],
                'name_last': current_user['name_last']
            }
        ],
        'messages': []
    }

    # Entry is added to data.py
    channels.append(new_channel)

    return {
        'channel_id': channel_id,
    }

import data

def check_if_valid_email(email):
    '''
    Given the email of the user to be registeredd checks if it is a valid email
    using a regex
    '''

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    return False

def check_if_valid_password(password):
    '''
    Given the password of the user to be registered checks it's length is in
    valid range and if it has printable ASCII characters only
    '''

    if not 6<= len(password) <= 32:
        return False
    if not password.isprintable():
        return False
    return True

def check_name_length_and_is_a_whitesapce(name_to_check):
    '''
    Given the first or last name of the user to be registered checks if it's
    length is in valid range and if it is not completely a whitespace
    '''

    if not 1 <= len(name_to_check) <= 50:
        return False
    if name_to_check.isspace():
        return False
    return True

def check_if_first_user():
    '''
    Chceks if the registering user is the first user of Flockr, this later leads
    to giving the first user the admin of Flockr status
    '''
    if len(data.data['users']) == 0:
        return True
    return False

def invalidating_token(token):
    '''
    Given the token of authenticated user invalidates it which later leads to
    unauthentication of the user i.e. logging-out the user
    '''

    for user in data.data['users']:
        if user['token'] == token:
            user['token'] = 'invalidated_the_token'
    return True

def get_channel_info(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel:
            return channel
    return False

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

def get_user_info(variable, identifier):
    for user in data.data['users']:
        if user[variable] == identifier:
            return user

    return False

def is_user_in_channel(u_id, channel_id):

    channel_info = get_channel_info(channel_id)
    user_info = get_user_info('u_id', u_id)

    user_data = {'u_id': user_info['u_id'], 'name_first': user_info['name_first'], 'name_last': user_info['name_last']}

    return user_data in channel_info['all_members']

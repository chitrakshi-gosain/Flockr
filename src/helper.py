import data

def check_if_valid_email(email):
    '''
    Given the email of the user to be registeredd checks if it is a valid email
    using a regex
    '''

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    #if re.search(regex, email):
    #    return True
    #return False
    return re.search(regex, email) #more concise


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
    #if len(data.data['users']) == 0:
    #    return True
    #return False
    return len(data.data['users']) == 0 #more concise


def invalidating_token(token):
    '''
    Given the token of authenticated user invalidates it which later leads to
    unauthentication of the user i.e. logging-out the user
    '''

    for user in data.data['users']:
        if user['token'] == token:
            user['token'] = 'invalidated_the_token' #I'm not sure if this directly affects data
    return True


def get_channel_info(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel:
            return channel
    return False


def is_user_authorised(token, u_id, channel_id):
    user_info = get_user_info('token', token)

    in_channel = is_user_in_channel(user_info['u_id'], channel_id)

    #user_authorised = False
    #for user in data.data['users']:
    #    if user['token'] == token:
    #        user_authorised = user['is_admin']

    #for member in channel_dict['all_members']:
    #    if member['u_id'] == u_id:
    #        user_authorised = True

    return user_info['is_admin'] or in_channel


def is_channel_owner(u_id, channel_id):
    #for channel in data.data['channels']:
    #    if channel["channel_id"] == channel_id and u_id in [owner["u_id"] for owner in channel["owner_members"]]:
    #        return True
    #return False

    channel_owners = get_channel_info(channel_id)['owner_members']
    return any(user['u_id'] == u_id for user in channel_owners)


def get_user_info(variable, identifier):
    for user in data.data['users']:
        if user[variable] == identifier:
            return user

    return False


def is_user_in_channel(u_id, channel_id):

    #channel_info = get_channel_info(channel_id)
    #user_info = get_user_info('u_id', u_id)

    #user_data = {
    #    'u_id': user_info['u_id'],
    #    'name_first': user_info['name_first'],
    #    'name_last': user_info['name_last']
    #}

    #return user_data in channel_info['all_members']

    channel_members = get_channel_info(channel_id)['channel_members']
    return any(user['u_id'] == u_id for user in channel_members)



'''
#### Channel_messages and channel_details helper functions
# Checking the validity of a token
def is_token_valid(token):
    valid_token = False
    for user in data.data['users']:
        if user['token'] == token:
            valid_token = True

    return valid_token

Use:
user_info = get_user_info('token', token)

if not user_info:
    #Token is invalid

or

if not get_user_info('token', token):
    #Token is invalid
'''


'''
# Checking the validity of a channel
def is_channel_valid(channel_id):

    channel_valid = False
    channel_dict = {}
    channel_info = [channel_valid, channel_dict]

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel_info[0] = True
            channel_info[1] = channel
            break

    return channel_info

Use:
channel_info = get_channel_info(channel_id)
if not channel_info:
    #channel is invalid
'''


'''
# Checking if the user is authorised
def is_user_authorised1(token, u_id, channel_dict):
    u_id = find_user_id(token)

    user_authorised = False
    for user in data.data['users']:
        if user['token'] == token:
            user_authorised = user['is_admin']

    for member in channel_dict['all_members']:
        if member['u_id'] == u_id:
            user_authorised = True

    return user_authorised

Use:
is_user_authorised(token, channel_id)
'''


'''
def find_user_dictionary(token):

    current_user = {}
    # Loops through users until matching token is found
    for user in data.data['users']:
        if user['token'] == token:
            current_user = user
    # If matching token is not found then AccessError is raised
    if current_user == {}:
        raise AccessError("Invalid Token")

    return current_user

Use:
user_info = get_user_info('token', token)
'''


'''
def find_user_id(token):
    for user in data.data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            return u_id

Use:
user_id = get_user_info('token', token)['u_id']
'''

'''
Created collaboratively by Wed15Team2 2020 T3
Contributers - Jordan Hunyh, Chitrakshi Gosain, Cyrus Wilkie,
               Ahmet Karatas, Joseph Knox

Iteration 1
'''

import re
import data

def check_if_valid_email(email):
    '''
    Given the email of the user to be registeredd checks if it is a
    valid email using a regex
    '''

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    #if re.search(regex, email):
    #    return True
    #return False
    return re.search(regex, email) #more concise


def check_if_valid_password(password):
    '''
    Given the password of the user to be registered checks it's length
    is in valid range and if it has printable ASCII characters only
    '''

    if not 6 <= len(password) <= 32:
        return False
    if not password.isprintable():
        return False

    return True


def check_name_length_and_is_a_whitesapce(name_to_check):
    '''
    Given the first or last name of the user to be registered checks if
    it's length is in valid range and if it is not completely a
    whitespace
    '''

    if not 1 <= len(name_to_check) <= 50:
        return False
    if name_to_check.isspace():
        return False

    return True


def check_if_first_user():
    '''
    Chceks if the registering user is the first user of Flockr, this
    later leads to giving the first user the admin of Flockr status
    '''
    #if len(data.data['users']) == 0:
    #    return True
    #return False
    return len(data.data['users']) == 0 #more concise


def invalidating_token(token):
    '''
    Given the token of authenticated user invalidates it which later
    leads to unauthentication of the user i.e. logging-out the user
    '''

    for user in data.data['users']:
        if user['token'] == token:
            user['token'] = 'invalidated_the_token' #I'm not sure if this directly affects data

    return True


def get_channel_info(channel_id):

    '''
    ADD DOCSTRING HERE
    '''

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return False


def is_user_authorised(token, u_id, channel_id):
    '''
    ADD DOCSTRING HERE
    '''

    user_info = get_user_info('token', token)

    in_channel = is_user_in_channel(user_info['u_id'], channel_id)

    # why are we taking u_id as a parameter, if not using it?, keep in
    # mind to change it whereever necessary

    #user_authorised = False
    #for user in data.data['users']:
    #    if user['token'] == token:
    #        user_authorised = user['is_admin']

    #for member in channel_dict['all_members']:
    #    if member['u_id'] == u_id:
    #        user_authorised = True

    return user_info['is_admin'] or in_channel


def is_channel_owner(u_id, channel_id):
    '''
    ADD DOCSTRING HERE
    '''

    #for channel in data.data['channels']:
    #    if channel["channel_id"] == channel_id and u_id in [owner["u_id"] \
    #    for owner in channel["owner_members"]]:
    #        return True
    #return False

    channel_owners = get_channel_info(channel_id)['owner_members']
    return any(user['u_id'] == u_id for user in channel_owners)


def get_user_info(variable, identifier):
    '''
    ADD DOCSTRING HERE
    '''

    for user in data.data['users']:
        if user[variable] == identifier:
            return user

    return False


def is_user_in_channel(u_id, channel_id):
    '''
    ADD DOCSTRING HERE
    '''

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

def is_token_valid(token):
    valid_token = False
    for user in data.data['users']:
        if user['token'] == token:
            valid_token = True

    return valid_token


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


def check_if_registered_user(email):
    '''
    Given the email of a user to be registered checks if the email is
    already being used by another user
    '''

    for user in data.data['users']:
        if user['email'] == email:
            return True

    return False


def get_user_id_from_email(email):
    '''
    Given the email of the user who is:
    -> already registered: finds the user by their email in the database
                           and returns their existing u_id
    -> to be registered: counts the number of existing users and assigns
                         the next number as u_id
    and then returns it
    '''

    user_count = -1
    for user in data.data['users']:
        if user['email'] == email:
            user_id = user['u_id']
            return user_id
        user_count += 1

    return user_count + 1


def generate_handle(name_first, name_last, email):
    '''
    Given the first and last name of the user, a handle is generated
    that is the concatentation of a lowercase-only first name and last
    name. If the concatenation is longer than 20 characters, it is
    cutoff at 20 characters. If the handle is already taken, user's u_id
    is concatenated at the very end, incase this concatenation exceeds
    the length of 20 characters, the last characters of handle string
    (which already belongs to another user) are adjusted to accomodate
    the user's u_id in the very end
    '''

    concatenated_names = name_first.lower() + name_last.lower()
    handle_string = concatenated_names[:20]
    status = False

    for user_with_same_handle in data.data['users']:
        if user_with_same_handle['handle_str'] == handle_string:
            status = True

    if status is True:
        user_id = str(get_user_id_from_email(email))
        cut_handle_till = 20 - len(user_id)
        handle_string = handle_string[:cut_handle_till] + user_id
    return handle_string


def check_password(email, password):
    '''
    Given the password of the user while logging-in matches the password
    with the database file which stores the password of user made while
    registering
    '''

    for user in data.data['users']:
        if user['email'] == email:
            if user['password'] == password:
                return True

    return False


def check_token(token):
    '''
    Given the token checks if the token belongs to an authenticated user
    '''

    for user in data.data['users']:
        if user['token'] == token:
            return True

    return False


# later modify this as store_And_generate_token(email):, i.e. this will generate
# token, store it and then return it
def store_generated_token(email, user_token):
    '''
    Given the email of the user trying of log-in stores the
    authenticated token in database as necessary which later results in
    the authentication of the user for the particular session
    '''

    for user in data.data['users']:
        if user['email'] == email:
            user['token'] = user_token

'''
Created collaboratively by Wed15Team2 2020 T3
Contributors - Jordan Hunyh, Chitrakshi Gosain, Cyrus Wilkie,
               Ahmet Karatas, Joseph Knox

Iteration 1
'''

import re
import data

# CONSTANTS
MIN_LENGTH_PASSWORD = 6
MAX_LENGTH_PASSWORD = 32

def check_if_valid_email(email):
    '''
    Given the email of the user to be registered checks if it is a
    valid email using a regex
    '''

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.search(regex, email) #more concise
    # this returns None instead of False.. :/


def check_if_valid_password(password):
    '''
    Given the password of the user to be registered checks it's length
    is in valid range and if it has printable ASCII characters only
    '''

    if not MIN_LENGTH_PASSWORD <= len(password) <= MAX_LENGTH_PASSWORD:
        return False
    if not password.isprintable():
        return False

    return True


def check_string_length_and_whitespace(min_length, max_length, name_to_check):
    '''
    Given the first or last name of the user to be registered checks if
    it's length is in valid range and if it is not completely a
    whitespace
    '''

    if not min_length <= len(name_to_check) <= max_length:
        return False
    if name_to_check.isspace():
        return False

    return True


def invalidating_token(token):
    '''
    Given the token of authenticated user invalidates it which later
    leads to un-authentication of the user i.e. logging-out the user
    '''

    for user in data.data['users']:
        if user['token'] == token:
            user['token'] = 'invalidated_the_token'

    return True


def get_channel_info(channel_id):

    '''
    Given a potential channel_id, returns the channel dictionary
    of the matching channel, else returns false

    Example:
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError('channel does not exist')
    if channel_info['is_public']:
        pass
    '''

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return False


def is_user_authorised(token, channel_id):
    '''
    Given a VALID token and VALID channel_id, returns True if the
    user is in the channel or if the user is admin

    (You should check if these arguments are valid before calling the functions)
    '''

    user_info = get_user_info('token', token)

    is_owner = is_channel_owner(user_info['u_id'], channel_id)

    return user_info['is_admin'] or is_owner


def is_channel_owner(u_id, channel_id):
    '''
    Given a VALID user id and VALID channel_id, returns True
    if the user is an owner of the channel, else returns False

    (You should check if these arguments are valid before calling the functions)
    '''

    channel_owners = get_channel_info(channel_id)['owner_members']
    return any(user['u_id'] == u_id for user in channel_owners)


def get_user_info(variable, identifier):
    '''
    Given a VALID variable ('u_id', 'token', 'email') and potential
    UNIQUE identifier (u_id, token, email), returns the user dictionary.
    Else returns False
    '''

    for user in data.data['users']:
        if user[variable] == identifier:
            return user

    return False

def is_user_in_channel(u_id, channel_id):
    '''
    Given a VALID user id and VALID channel id, returns True if
    the user is within the specified channel

    (You should check if these arguments are valid before calling the functions)
    '''

    channel_members = get_channel_info(channel_id)['all_members']
    return any(user['u_id'] == u_id for user in channel_members)

def get_message_info(message_id):
    '''
    Given a potential message_id, returns the message dictionary
    of the matching channel, else returns false

    Example:
    message_info = helper.get_channel_info(channel_id)
    if not message_info:
        raise InputError('message does not exist')
    '''

    for channel in data.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return message

    return False

def update_data(keyword, user_id, identifier):
    '''
    Given a VALID variable ('name_first'|'name_last'|'email'|'handle_str'),
    u_id of the user who wants to update his/her data and potential
    UNIQUE identifier (name_first|name_last|email|handle_str), updates
    their data under data['users'] in data.py
    '''

    for user in data.data['users']:
        if user['u_id'] == user_id:
            user[keyword] = identifier

########################################################################################

'''
def generate_handle(name_first, name_last, email):

    Given the first and last name of the user, a handle is generated
    that is the concatentation of a lowercase-only first name and last
    name. If the concatenation is longer than 20 characters, it is
    cutoff at 20 characters. If the handle is already taken, user's u_id
    is concatenated at the very end, incase this concatenation exceeds
    the length of 20 characters, the last characters of handle string
    (which already belongs to another user) are adjusted to accomodate
    the user's u_id in the very end


    concatenated_names = name_first.lower() + name_last.lower()
    handle_string = concatenated_names[:20]
    status = False

    for user_with_same_handle in data.data['users']:
        if user_with_same_handle['handle_str'] == handle_string:
            status = True

    if status is True:
        user_id = str(len(data.data['users']))
        cut_handle_till = 20 - len(user_id)
        handle_string = handle_string[:cut_handle_till] + user_id
    return handle_string
'''

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

    #user = get_user_info('email', 'dhwu@hjufe')
    #return user['password'] == password



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

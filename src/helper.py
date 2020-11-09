'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Jordan Hunyh, Chitrakshi Gosain, Cyrus Wilkie,
               Ahmet Karatas, Joseph Knox

Iteration 1
'''

import re
import hashlib
import jwt
from datetime import datetime
import data
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
This file contains all the helper functions used throughout the 
implementation of interface
'''

# CONSTANTS
MIN_LENGTH_PASSWORD = 6
MAX_LENGTH_PASSWORD = 32
SECRET = 'wed15grapeteam2' * 3

def check_if_valid_email(email):
    '''
    Given the email of the user to be registered checks if it is a
    valid email using a regex
    '''

    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
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

    return False

def get_channel_info(channel_id):

    '''
    Given a potential channel_id, returns the channel dictionary
    of the matching channel, else returns false

    Example:
    channel_info = helper.get_channel_info(channel_id)
    if not channel_info:
        raise InputError(description='channel does not exist')
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

    if variable == 'token':
        try:
            identifier = decode_encoded_token(identifier)
        except:
            return False

    for user in data.data['users']:
        if user[variable] == identifier:
            return user

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
        raise InputError(description='message does not exist')
    '''

    for channel in data.data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return message

    return False

def encrypt_password_with_hash(password):
    '''
    Given the password of the user encrypts it using hashlib for secured
    authentication
    '''

    return hashlib.sha256(password.encode()).hexdigest()

def generate_encoded_token(user_id):
    '''
    Given the u_id of the user trying of log-in stores the
    authenticated token in database as necessary which later results in
    the authentication of the user for the particular session
    '''

    try:
        unique_token = {
            'u_id': str(user_id),
            'iat': datetime.utcnow()
        }

        encoded_token = jwt.encode(unique_token, SECRET, algorithm=\
            'HS256').decode('utf-8')

        data.data['valid_tokens'].append({
            encoded_token: int(unique_token['u_id'])
        })

        return encoded_token
    except:
        raise InputError(description='Token is expected to be the user-id of user')

def decode_encoded_token(token):
    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET, algorithms='HS256')

        return payload['u_id']
    except:
        raise AccessError(description='Token passed in is not a valid token')  

def post_message_to_channel(message, channel_id):
    '''
    Posts a message already present in data['messages'] to the relevant channel
    '''
    channel = get_channel_info(channel_id)
    channel['messages'].append(message)
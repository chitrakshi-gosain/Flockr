'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Cyrus Wilkie, Jordan Hunyh

Iteration 1 & 2
'''

import data
from helper import get_user_info, is_user_in_channel
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> users_all(token) return {users}
-> admin_userpermission_change(token, u_id, permission_id) return {}
-> search(toke, query_str) return {messages}
-> clear() return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> u_id: integer
    -> permission_id: integer
    -> query_str:string
    -> users: list of dictionaries, where each dictionary contains types
              u_id, email, name_first, name_last, handle_str
    -> messages: list of dictionaries, where each dictionary contains
                 types message_id, u_id, message, time_created
'''

# CONSTANTS
OWNER = 1
USER = 2

def clear():
    '''
    DESCRIPTION:
    Resets the internal data of the application to it's initial state
    '''

    data.data = {
        'users': [],
        'channels': [],
        'messages': [],
        'valid_tokens': [],
        'reset_codes': {},
        'password_record': {}
    }


def users_all(token):
    '''
    DESCRIPTION:
    Returns a list of all users and their associated details

    PARAMETERS:
        -> token : token of a user

    RETURN VALUES:
        -> user : information about all the users

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    # Checking token validity
    caller = get_user_info('token', token)

    if not caller:
        raise AccessError(description='Token passed in is not a valid token')

    # Processing and appending each user dictionary entry
    # to the appropriate return format dictionary
    return_dict = {
        'users': [],
    }

    for user in data.data['users']:
        curr_user = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'profile_img_url': user['profile_img_url'],
            }

        return_dict['users'].append(curr_user)

    return return_dict

def admin_userpermission_change(token, u_id, permission_id):
    '''
    DESCRIPTION:
    Given a User by their user ID, set their permissions to
    new permissions described by permission_id

    PARAMETERS:
        -> token : token of user who called invite
        -> u_id : id of the user who is to be invited
        -> permission_id : id of the permission (1 == Owner, 2 == user)

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
         -> when the authorised user is not an owner
    Error type: InputError
    -> u_id does not refer to a valid user
    -> permission_id does not refer to a value permission
    '''

    #order of checks: invalid token, invalid user, invalid permission_id, invoker is admin
    invoker_info = get_user_info('token', token)
    if not invoker_info:
        raise AccessError(description='Token passed in is not a valid token')

    user_info = get_user_info('u_id', u_id)
    if not user_info:
        raise InputError(description='u_id does not refer to valid user')

    if not invoker_info['is_admin']:
        raise AccessError(description='invoker is not an admin')

    admin_count = len(list(filter(lambda user: user['is_admin'], data.data['users'])))

    if permission_id == OWNER:
        user_info['is_admin'] = True

    elif (permission_id == USER):
        if admin_count > 1: #there has to be at least 1 admin
            user_info['is_admin'] = False

    else:
        raise InputError(description='permission_id is invalid')

def search(token, query_str):
    '''
    DESCRIPTION:
    Given a query string, return a collection of messages in
    all of the channels that the user has joined that match the query

    Parameters:
        -> token : token of the invoker
        -> query_str : the target string to search with

    RETURN VALUES:
        -> messages : all messages that contain query_str

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    #find channels user is part of and add messages
    visible_messages = []

    for channel in data.data['channels']:
        if is_user_in_channel(user_info['u_id'], channel['channel_id']) or user_info['is_admin']:
            visible_messages += channel['messages']

    return {'messages': list(filter(lambda message: query_str in message['message'], visible_messages)) }

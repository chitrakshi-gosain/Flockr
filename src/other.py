import data
import helper
from error import AccessError, InputError
# this is not official implementation, this is just to use in my tests.
# therefore i made not tests for this

def clear():
    data.data = {'users': [], 'channels': []}

def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    DESCRIPTION:
    Given a User by their user ID, set their permissions to
    new permissions described by permission_id

    PARAMETERS:
        -> token : token of user who called invite
        -> u_id : id of the user who is to be invited
        -> permission_id : id of the permission (1 == Owner, 2 == user)

    RETURN VALUES:
    '''
    #order of checks: invalid token, invalid user, invalid permission_id, invoker is admin
    invoker_info = helper.get_user_info('token', token)
    if not invoker_info:
        raise AccessError('invalid token')

    user_info = helper.get_user_info('u_id', u_id)
    if not user_info:
        raise InputError('u_id does not refer to valid user')

    if not invoker_info['is_admin']:
        raise AccessError('invoker is not an admin')


    admin_count = len(list(filter(lambda user: user['is_admin'], data.data['users'])))

    if permission_id == 1:
        user_info['is_admin'] = True

    elif (permission_id == 2):
        if admin_count > 1: #there has to be at least 1 admin
            user_info['is_admin'] = False

    else:
        raise InputError('permission_id is invalid')

def search(token, query_str):
    '''
    DESCRIPTION:
    Given a query string, return a collection of messages in
    all of the channels that the user has joined that match the query

    Parameters:
        -> token : token of the invoker
        -> query_str : the target string to search with

    RETURN VALUES:
        -> { messages } : all messages visible to the user that contains query_str
    '''
    user_info = helper.get_user_info('token', token)
    if not user_info:
        raise AccessError('invalid token')

    #find channels user is part of and add messages
    visible_messages = []

    for channel in data.data['channels']:
        if helper.is_user_in_channel(user_info['u_id'], channel['channel_id']) or user_info['is_admin']:
            visible_messages += channel['messages']

    return {'messages': list(filter(lambda message: query_str in message['message'], visible_messages)) }

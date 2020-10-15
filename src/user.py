# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 2

import data
import helper
from error import InputError, AccessError

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
-> user_profile_sethandle(token, handle_str) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> u_id: integer
    -> user: dictionary containing u_id, email, name_first, name_last, handle_str
    -> name_first: string
    -> name_last: string
    -> email: string
    -> handle_str: string
'''

'''
EXCEPTIONS
    * user_profile

    * user_profile_setname
        Error type: InputError
            -> name_first is not between 1 and 50 characters inclusively in length
            -> name_last is not between 1 and 50 characters inclusively in length
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_setemail

    * user_profile_sethandle
'''

def user_profile(token, u_id):
    '''
    DESCRIPTION:
    For a valid user, returns information about
    their user_id, email, first name, last name,
    and handle

    PARAMETERS:
        -> token, u_id

    RETURN VALUES:
        -> {user}

    EXCEPTIONS:
        -> AccessError: Invalid token
        -> InputError: User with u_id is not a valid user
    '''

    # Checking token validity
    user = helper.get_user_info('token', token)
    if not user:
        raise AccessError('Invalid Token')

    # Checking u_id validity and getting user data
    user = helper.get_user_info('u_id', u_id)
    if not user:
        raise InputError('Not a valid user')

    return {
        'user': {
        	'u_id': u_id,
        	'email': user['email'],
        	'name_first': user['name_first'],
        	'name_last': user['name_last'],
        	'handle_str': user['handle_str'],
        },
    }

def user_profile_setname(token, name_first, name_last):
    '''
    DESCRIPTION:
    Given a token, replaces the authorised user's first and last name
    with the provided name_first and name_last respectively.

    PARAMETERS:
        -> token : token of user who called the function
        -> name_first : replacement first name
        -> name_last : replacement last name

    RETURN VALUES:
    '''

    # check if token is valid
    user_info = helper.get_user_info("token", token)
    if not user_info:
        raise AccessError('invalid token')

    # check if name_first and name_last are of invalid length
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Invalid length of first name")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Invalid length of last name")

    u_id = user_info["u_id"]

    for user in data.data["users"]:
        if user["u_id"] == u_id:
            user["name_first"] = name_first
            user["name_last"] = name_last
            break

    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }

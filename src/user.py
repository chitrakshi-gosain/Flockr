from helper import get_user_info
from error import AccessError, InputError

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
    user = get_user_info('token', token)

    if user == False:
        raise AccessError('Invalid Token')

    # Checking u_id validity and getting user data
    user = get_user_info('u_id', u_id)

    if user == False:
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
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }
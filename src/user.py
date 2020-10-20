'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Cyrus Wilkie, Chitrakshi Gosain, Joseph Knox

Iteration 2
'''

from error import InputError, AccessError
from helper import get_user_info, check_if_valid_email, \
check_string_length_and_whitespace, update_data, decode_encoded_token

'''
****************************BASIC TEMPLATE******************************
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
    -> user: dictionary containing u_id, email, name_first, name_last,
             handle_str
    -> name_first: string
    -> name_last: string
    -> email: string
    -> handle_str: string
'''

'''
EXCEPTIONS
    * user_profile
        Error type: InputError
            -> insufficient parameters
            -> user with u_id is not a valid_user
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_setname
        Error type: InputError
            -> insufficient parameters
            -> name_first is not between 1 and 50 characters inclusively
               in length
            -> name_last is not between 1 and 50 characters inclusively
               in length
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_setemail
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email address is already being used by another user
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_sethandle
        Error type: InputError
            -> insufficient parameters
            -> handle_str must be between 3 and 20 characters
            -> handle is already being used by another user
        Error type: AccessError
            -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
-> allow multiple session log-ins,
   * for this make a data.data['valid_tokens'] dict in data.py, have
   tokens as key, and value as u_id this way we can keep track of
   multiple logins very easily, but don't do it now everyone will have to
   change implementation, do it after we are done merging all branches
   once, so if anything ever goes wrong we have A BACKUP. also, this
   ain't imp for itr 1 so don't stress. :)
'''

# CONSTANTS
MIN_CHAR_NAME_FIRST = 1
MAX_CHAR_NAME_FIRST = 50
MIN_CHAR_NAME_LAST = 1
MAX_CHAR_NAME_LAST = 50
MIN_CHAR_HANDLE_STR = 3
MAX_CHAR_HANDLE_STR = 20

def user_profile(token, u_id):
    '''
    DESCRIPTION:
    For a valid user, returns information about
    their user_id, email, first name, last name,
    and handle

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> u_id : user id of a user

    RETURN VALUES:
        -> user : dictionary containing u_id, email, name_first,
                  name_last, handle_str of the user
    '''

    # Checking token validity
    user = get_user_info('token', token)
    if not user:
        raise AccessError(description='Token passed in is not a valid token')

    # Checking u_id validity and getting user data
    user = get_user_info('u_id', u_id)
    if not user:
        raise InputError(description='User with u_id is not a valid user')

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
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> name_first : new first name of a user
        -> name_last : new last name of a user
    '''

    # check if token is valid
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    # check if name_first and name_last are of invalid length
    if not check_string_length_and_whitespace(MIN_CHAR_NAME_FIRST, \
                                             MAX_CHAR_NAME_FIRST, name_first):
        raise InputError(description='name_first is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    if not check_string_length_and_whitespace(MIN_CHAR_NAME_LAST, \
                                             MAX_CHAR_NAME_LAST, name_last):                                             
        raise InputError(description='name_last is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    update_data('name_first', user_info['u_id'], name_first)
    update_data('name_last', user_info['u_id'], name_last)

    return {
    }


def user_profile_setemail(token, email):
    '''
    DESCRIPTION:
    Updates the authorized user's email address

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> email : new email of a user
    '''

    # Checking for InputError(s) or AccessError:
    if None in {token, email}:
        raise InputError(description='Insufficient parameters. Please enter: \
        token, email')

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    if user_info['email'] == email:
        return {
        }

    if get_user_info('email', email):
        raise InputError(description='Email address is already being used by \
        another user')

    # Since there is no InputError or AccessError, hence proceeding
    # forward:

    update_data('email', user_info['u_id'], email)

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    DESCRIPTION:
    Updates the authorized user's handle (i.e. display name)

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> handle_str : new handle_str of a user
    '''

    # Checking for InputError(s) or AccessError:
    if None in {token, handle_str}:
        raise InputError(description='Insufficient parameters. Please enter: \
        token, handle_str')

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    if not check_string_length_and_whitespace(MIN_CHAR_HANDLE_STR, \
                                             MAX_CHAR_HANDLE_STR, handle_str):
        raise InputError(description='handle_str is not between 3 and 20 \
        characters inclusively in length or is a whitespace')

    if user_info['handle_str'] == handle_str:
        return {
        }

    if get_user_info('handle_str', handle_str):
        raise InputError(description='Handle is already being used by \
        another user')

    # Since there is no InputError or AccessError, hence proceeding
    # forward:

    update_data('handle_str', user_info['u_id'], handle_str)

    return {
    }

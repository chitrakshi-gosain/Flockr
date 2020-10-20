'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import data
from error import InputError, AccessError
from helper import check_if_valid_email, check_if_valid_password, \
check_string_length_and_whitespace, invalidating_token, get_user_info, \
encrypt_password_with_hash, generate_encoded_token, decode_encoded_token

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> email: string
    -> password: string
    -> name_first: string
    -> name_last: string
    -> token: string
    -> u_id: integer
    -> is_success: boolean
'''

'''
EXCEPTIONS
    * auth_login
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email entered does not belong to a user
            -> password is not correct
    * auth_logout
        Error type: InputError
            -> insufficient parameters
        Error type: AccessError
            -> token passed in is not a valid token
    * auth_register
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email address is already being used by another user
            -> password entered is less than 6 characters long or more
               than 32 characters long
            -> name_first is not between 1 and 50 characters inclusively
               in length
            -> name_last is not between 1 and 50 characters inclusively
               in length
'''

'''
KEEP IN MIND:
-> make one function to check if user is registered and use it for both
   re-registration check and registered before login check
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
MAX_CHAR_HANDLE_STR = 20

def auth_login(email, password):
    '''
    DESCRIPTION:
    Given a registered user's email and password and generates a valid
    token for the user to remain authenticated

    PARAMETERS:
        -> email : email-id of user
        -> password : password of the user

    RETURN VALUES:
        -> u_id : user-id of the user
        -> token : token to authenticate the user
    '''

    # Checking for InputError(s):
    if None in {email, password}:
        raise InputError(description='Insufficient parameters, please enter: \
        email, password')

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    user_info = get_user_info('email', email)

    if not user_info:
        raise InputError(description='Email entered does not belong to a user')

    if not user_info['password'] == encrypt_password_with_hash(password):
        raise InputError(description='Password is not correct')

    # Since there are no InputError(s), hence proceeding forward:

    # returning the dictionary with users' u_id, and encoded token
    # authenticated for their session
    return {
        'u_id': user_info['u_id'],
        'token': generate_encoded_token(user_info['u_id'])
    }

def auth_logout(token):
    '''
    DESCRIPTION:
    Given an active token, invalidates the token to log the user out. If
    a valid token is given, and the user is successfully logged out, it
    returns true, otherwise false

    PARAMETERS:
        -> token : token of the authenticated user

    RETURN VALUES:
        -> is_success : True if user is successfully logged out,
                        otherwise False
    '''

    # Checking for InputError:
    if not token:
        raise InputError(description='Insufficient parameters. Please enter: \
                        token')

    # Checking for AccessError:
    if not get_user_info('token', token):
        raise AccessError(description='Token passed in is not a valid token')

    # Since there is no InputError or AccessError, hence proceeding
    # forward:

    return {
        'is_success': invalidating_token(decode_encoded_token(token))
    }

def auth_register(email, password, name_first, name_last):
    '''
    DESCRIPTION:
    Given a user's first and last name, email address, and password,
    creates a new account for them and returns a new token for
    authentication in their session. A handle is generated that is the
    concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20
    characters. If the handle is already taken, user's u_id is
    concatenated at the very end, incase this exceeds the length of 20
    characters, the last characters of handle string are adjusted to
    accommodate the user's u_id

    PARAMETERS:
        -> email : email-id of user
        -> password : password of the user
        -> name_first : first name of the user
        -> name_last : last name of the user

    RETURN VALUES:
        -> u_id : user-id of the user
        -> token : token to authenticate the user
    '''

    # Checking for InputError(s):
    if None in {email, password, name_first, name_last}:
        raise InputError(description='Insufficient parameters. Please enter: \
        email, password, name_first, name_last')

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    if not check_if_valid_password(password):
        raise InputError(description='Password entered is less than 6 \
        characters long or more than 32 characters long or contains Non-ASCII \
            characters')

    if not check_string_length_and_whitespace(MIN_CHAR_NAME_FIRST, \
                                              MAX_CHAR_NAME_FIRST, name_first):
        raise InputError(description='name_first is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    if not check_string_length_and_whitespace(MIN_CHAR_NAME_LAST, \
                                                MAX_CHAR_NAME_LAST, name_last):
        raise InputError(description='name_last is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    if get_user_info('email', email):
        raise InputError(description='Email address is already being used by \
        another user')

    # Since there are no InputError(s), hence proceeding forward:

    # Generating handle_str
    concatenated_names = name_first.lower() + name_last.lower()
    handle_string = concatenated_names[:MAX_CHAR_HANDLE_STR]
    status = False

    for user_with_same_handle in data.data['users']:
        if user_with_same_handle['handle_str'] == handle_string:
            status = True

    if status:
        user_id = str(len(data.data['users']))
        cut_handle_till = MAX_CHAR_HANDLE_STR - len(user_id)
        handle_string = handle_string[:cut_handle_till] + user_id

    # making a new dictionary for new_user and adding values to the keys
    # respectively some keys' values are parameters from the user, others are
    # obtained using both helper functions and user's innput(as parameters
    # for these)
    new_user = {
        'u_id' : len(data.data['users']),
        'is_admin' : bool(len(data.data['users']) == 0),
        'email' : email,
        'name_first' : name_first,
        'name_last' : name_last,
        'handle_str' : handle_string,
        'token' : str(len(data.data['users'])),
        'password' : encrypt_password_with_hash(password)
    }

    # appending the data of new_user to data dictionary in data file
    data.data['users'].append(new_user)

    # logging-in the new_user to get the authenticated token for their
    # current session
    user_login_credentials = auth_login(email, password)

    return {
        'u_id': user_login_credentials['u_id'],
        'token': user_login_credentials['token']
    }

'''
WHITE BOX TESTING FOR CHECKING IF IMPLEMENTATION IS AS EXPECTED

if __name__ == '__main__':
    # check_for_admin_status_of_first_user
    clear()
    user1 = auth_register('registerationtestvalidemailid0@gmail.com', \
                         '123Abc!0', 'Valid', 'User0')
    user2 = auth_register('registerationtestvalidemailid1@gmail.com', \
                         '123Abc!1', 'Valid', 'User1')
    for user in data.data['users']:
        if user['u_id'] == user1['u_id']:
            user1_admin_status = user['is_admin']
        if user['u_id'] == user2['u_id']:
            user2_admin_status = user['is_admin']
    assert user1_admin_status != user2_admin_status
    print(user1_admin_status, user2_admin_status)
'''

# NOT NEEDED ATM:

# def check_if_valid_password(password):
#     allowed_special_symbols = ['!', '@', '#', '$', '%', '^', '&', '*']

#     if not 6 <= len(password) <= 32:
#         return False

#     if not any(character.isdigit() for character in password):
#         return False

#     if not any(character.isupper() for character in password):
#         return False

#     if not any(character.islower() for character in password):
#         return False

#     if not any(character in allowed_special_symbols for character in \
#               password):
#         return False

#     return True


# code used to debug logout :     print(token)
#                                 print(check_token(token)

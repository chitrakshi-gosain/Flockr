'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1 & 3
'''

from uuid import uuid4
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
-> auth_passwordreset_request(email) return {}
-> auth_passwordreset_reset(reset_code, new_password) return {}
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
    -> reset_code: string
    -> new_password: string
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
-> new key 'reset_codes' in data.data to store 'reset_code : email'
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

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email entered does not belong to a user
        -> password is not correct
    '''

    # Checking for InputError(s):

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    user_info = get_user_info('email', email)

    if not user_info:
        raise InputError(description='Email entered does not belong to a user')

    if not user_info['password'] == encrypt_password_with_hash(password):
        raise InputError(description='Password is not correct')

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

    # generating a valid token
    user_info['token'] = str(user_info['u_id'])

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

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    # Checking for AccessError:
    if not get_user_info('token', token):
        raise AccessError(description='Token passed in is not a valid token')

    # Since there is no AccessError, hence proceeding forward:

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

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email address is already being used by another user
        -> password entered is less than 6 characters long or more
            than 32 characters long
        -> name_first is not between 1 and 50 characters inclusively
            in length
        -> name_last is not between 1 and 50 characters inclusively
            in length
    '''

    # Checking for InputError(s):

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

    # Since there are no AccessError or InputError(s), hence proceeding
    # forward:

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

    # encrypting the password and adding it to his password record
    encrypted_password = encrypt_password_with_hash(password)
    data.data['password_record'][email] = {encrypted_password}

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
        'token' : 'no_token_generated',
        'password' : encrypted_password,
        'profile_img_url': ''
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

def auth_passwordreset_request(email):
    '''
    DESCRIPTION:
    Given an email address, if the user is a registered user, generates
    a reset code, stores it the database and returns it, which is then
    incorporated in the reset email

    PARAMETERS:
        -> email : email of a user

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email entered does not belong to a user
    '''

    # Checking for InputError(s):

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    user_info = get_user_info('email', email)

    if not user_info:
        raise InputError(description='Email entered does not belong to a user')

    # Since there is no InputError(s), hence proceeding forward:

    # generating and saving reset_code in data.py for later use
    reset_code = uuid4().hex.upper()[0:6]
    data.data['reset_codes'][reset_code] = email

    return reset_code

def auth_passwordreset_reset(reset_code, new_password):
    '''
    DESCRIPTION:
    Given a reset code for a user, set that user's new password to the
    password provided

    PARAMETERS:
        -> reset_code : reset code provided to user for password reset
        -> new_password : new password of user

    EXCEPTIONS:
    Error type: InputError
        -> reset_code is not a valid reset_code
        -> password entered is not a valid password
        -> password entered is similar to one of the old passwords
    '''

    # Checking for InputError(s):

    if reset_code not in data.data['reset_codes'].keys():
        raise InputError(description='Reset code is not a valid code')

    if not check_if_valid_password(new_password):
        raise InputError(description='Password entered is less than 6 \
        characters long or more than 32 characters long or contains Non-ASCII \
            characters')

    new_password = encrypt_password_with_hash(new_password)

    email = data.data['reset_codes'][reset_code]
    prev_password_list = data.data['password_record'][email]
    print(prev_password_list)
    print(new_password)
    if new_password in prev_password_list:
        raise InputError(description='Password entered is similar to one of \
        the old passwords')

    # Since there are no InputError(s), hence proceeding forward:

    # changing the password
    user_info = get_user_info('email', email)
    user_info['password'] = new_password

    # adding user's new_password to his password record
    data.data['password_record'][email].add(new_password)

    return {
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

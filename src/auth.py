# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain
# Reviewer - Ahmet K

# Iteration 1
'''
*********************************BASIC TEMPLATE*********************************
'''

'''
EXCEPTIONS
Error type: InputError
-> email entered is not valid
-> email entered does not belong to a user, i.e. not registered
-> password is incorrect
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> user can be already logged-in and trying to re-log-in, this has two 
possibilties:
        *log-in to self account again
        *log-in to someone else's account
however, in both cases user should be asked to logout first and then try.

'''

'''
DATA TYPES 
-> email: string
-> password: string
-> name_first: string
-> name_last: string
-> token: string
-> u_id: inetger
-> is_success: boolean
'''

import re
from data import *
from error import InputError

def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    if None in {email, password, name_first, name_last}:
        raise InputError(
            description = 'Insufficient parameters. Please enter: email, password, name_first, name_last'
        )

    if not check_if_valid_email(email):
         raise InputError(
            description = 'Please enter a valid email-id.'
        ) 

    if len(password) < 6 or len(password) > 32:
        raise InputError(
            description = 'Password should be of atleast 6 characters and no more than 32 chracters'
        )

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            description = 'First name should be between 1 to 50 characters'
        )
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            description = 'Last name should be between 1 to 50 characters'
        )

    if check_if_registered_user(email):
        raise InputError(
            description = 'Email address is already beng used by another user'
        )

    for user_id in data['users']:
        user_id += 1

    user_is_admin = False

    user_handle_str = generate_handle(name_first, name_last)

    user_token = name_first + name_last

    # making a new_user dictionary
    new_user = {
            'u_id' : user_id,
            'is_admin' : user_is_admin,
            'email' : email,
            'name_first' : name_first,
            'name_last' : name_last,
            'handle_str' : user_handle_str,
            'token' : user_token,
            'password' : password
    }
# IMPORTANT: rememeber to tell jordan to change handle_str in data, it's not like spec says
    data['users'].append(new_user)
    # things to be added to data['users']  -> just append to dictionary's key :))
    # -> u_id, is_admin (this will be false), email, name_first, name_last, handle_str, token, password
    # this is where we add data to data.data['users']
    
    return {
        'u_id': user_id,
        'token': user_token
    }

def check_if_valid_email(email):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    return False

def check_if_registered_user(email):
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

def generate_handle(name_first, name_last):
    concatenated_names = name_first + name_last
    handle_str = concatenated_names[:20]
    return handle_str

def check_password(x):
    pass

def check_name_length(y):
    pass
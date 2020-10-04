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
-> make one function to check if user is registered and use it for both 
   re-registration check and registered before login check
-> allow multiple session log-ins, 
   * for this make a data.data['valid_tokens'] dict in data.py, have tokens as 
   key, and value as u_id this way we can keep track of multiple logins very 
   easily, but dont do it now everyone will have to change implementation, do it
   after we are done merging all branches once, so if anything ever goes wrong 
   we have A BACKUP. also, this aint imp for itr 1 so dont stress. :)

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
import data
from error import InputError, AccessError

def auth_login(email, password):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    # Checking for InputError(s):
    if None in {email, password}:
        raise InputError('Insufficient parameters. Please enter: email, password.')

    if not check_if_valid_email(email):
         raise InputError('Please enter a valid email-id.') 

    if check_if_registered_user(email) is False:
        raise InputError('Please register since you are not registered yet.')

    if check_password(email, password) is False:
        raise InputError('Please enter the correct password.') 

    # Since there are no InputError(s), hence proceeding forward:
    
    # getting the return value 'u_id' from data
    user_id = get_user_id(email)

    # generating token
    user_token = email

    # updating token in data.data['users']
    store_generated_token(email, user_token)

    # returning the dictionary with users' u_id, and token authenticated for 
    # their session
    return {
        'u_id': user_id,
        'token': user_token
    }

def auth_logout(token):
    ''' 
    Logs out the user i.e. invalidates the authorised token of the user for the 
    session and returns a dictionary with is_success as key and value as True if
    successfully logged out, and value as False if not
    '''

    # Checking for InputError:
    if token is None:
        raise InputError('Insufficient parameters. Please enter: token')

    # Checking for AccessError:
    if not check_token(token):
        raise AccessError('No such token exists')

    # Since there is no InputError or AccessError, hence proceeding forward:

    status = invalidating_token(token)

    return {
        'is_success': status
    }

def auth_register(email, password, name_first, name_last):
    # Checking for InputError(s):
    if None in {email, password, name_first, name_last}:
        raise InputError('Insufficient parameters. Please enter: email, password, name_first, name_last')

    if not check_if_valid_email(email):
         raise InputError('Please enter a valid email-id.') 

    if not (6<= len(password) <= 32):
        raise InputError('Password should be of atleast 6 characters and no more than 32 chracters. Also, it should contain minimum one lowercase letter, one uppercase letter, one digit and one special character from the ones mentioned: "!, @, #, $, %, ^, &, *".')

    if not check_name_length(name_first):
        raise InputError('First name should be between 1 to 50 characters')

    if not check_name_length(name_last):
        raise InputError('Last name should be between 1 to 50 characters')

    if check_if_registered_user(email) is True:
        raise InputError('Email address is already being used by another user')
 
    # Since there are no InputError(s), hence proceeding forward:
         
    # Storing data required for creation of new_user in variables
    # user_id = get_user_id(email)
    # user_is_admin = False
    # user_handle_str = generate_handle(name_first, name_last)
    # user_token = '**token_not_assigned**'

    # making a new dictionary for new_user and adding all values to their keys : previously (with variables)
    # amking a new dictionary for new_user and adding values to the keys respectively
    # some keys' values are parameters from the user pthers are obtained using both user's input and helper fucntions (now)
    new_user = {
            'u_id' : get_user_id(email),
            'is_admin' : check_if_first_user(),
            'email' : email,
            'name_first' : name_first,
            'name_last' : name_last,
            'handle_str' : generate_handle(name_first, name_last),
            'token' : '**token_not_assigned**',
            'password' : password
    }

    # appending the data of new_user to data dictionary in data file
    data.data['users'].append(new_user)

    # logging-in the new_user to get the authenticated token for their current 
    # session
    user_login_credentials = auth_login(email, password)  

    return {
        'u_id': get_user_id(email),
        'token': user_login_credentials['token']  
    }

def check_if_valid_email(email):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    return False          

def check_name_length(name_to_check):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    if not 1 <= len(name_to_check) <= 50:
        return False
    return True

def check_if_registered_user(email):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    for user in data.data['users']:
        if user['email'] == email:
            return True
    return False

def get_user_id(email):
    '''
    NICE FUNCTION HEADER COMMENT HERE explain everything abt function here rather than in-line it doesnt look pretty
    '''
    user_count = -1
    for user in data.data['users']:
        # for an existing user, we find them by their email and return existing 
        # u_id
        if user['email']  == email:
            user_id = user['u_id']
            return user_id
        # counting the number of user(s) in data['users'], this helps in 
        # creating new u_id
        user_count += 1
    # for a new user, we make a new u_id and return it
    return user_count + 1

def generate_handle(name_first, name_last):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    concatenated_names = name_first + name_last
    handle_str = concatenated_names[:20]
    return handle_str

def check_password(email, password):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    for user in data.data['users']:
        if user['email']  == email:
            if user['password'] == password:
                return True
    return False

def check_token(token):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    for user in data.data['users']:
        if user['token'] == token:
            return True
    return False

# later make this as store_And_generate_token(email):, i.e. this will generate 
# token, store it and then return it
def store_generated_token(email, user_token):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    for user in data.data['users']:
            if user['email']  == email:
                user['token'] = user_token

# or do it this way, find the user with matching token and relace the token with invalid token string
def invalidating_token(token):
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    for user in data.data['users']:
        if user['token']  == token:
            user['token'] = 'invalidated_the_token'
            return True
    return False

def check_if_first_user():
    '''
    NICE FUNCTION HEADER COMMENT HERE
    '''
    if len(data.data['users']) == 0:
        return True
    return False

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
          
#     if not any(character in allowed_special_symbols for character in password): 
#         return False

#     return True

# code used to debug logout :     print(token)  
#                                 print(check_token(token))
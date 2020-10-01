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
    # Checking for InputError:
    if None in {token}:
        raise InputError('Insufficient parameters. Please enter: token')
    
    status = False
    # Checking for AccessError:
    if check_token(token) is False:
        return {
            'is_success': status
        }

    # if check_token(token) is False:
    #     raise AccessError('No such token exists')

    # status = False

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

    if not check_if_valid_password(password):
        raise InputError('Password should be of atleast 6 characters and no more than 32 chracters. Also, it should contain minimum one lowercase letter, one uppercase letter, one digit and one special character from the ones mentioned: "!, @, #, $, %, ^, &, *".')

    if not check_name_length(name_first):
        raise InputError('First name should be between 1 to 50 characters')

    if not check_name_length(name_last):
        raise InputError('Last name should be between 1 to 50 characters')

    if check_if_registered_user(email) is True:
        raise InputError('Email address is already being used by another user')
 
    # Since there are no InputError(s), hence proceeding forward:
    
       
    user_id = get_user_id(email)

    user_is_admin = False

    user_handle_str = generate_handle(name_first, name_last)

    # token generation is actually part of login so just call login here rather than making token
    # do:
    # user_login_credentials = {}
    # user_login_credentials= auth_login(email, password)
    # user_token = user_login_credentials['token']
    # but this wont technically work since user isnt registered yet, so have a 
    # invalid_token at first, then add the dict, then login then get token and return, voila
    user_token = 'invalid_token'

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
    data.data['users'].append(new_user.copy())
    # things to be added to data.data['users']  -> just append to dictionary's key :))
    # -> u_id, is_admin (this will be false), email, name_first, name_last, handle_str, token, password
    # this is where we add data to data.data['users']

    user_login_credentials= auth_login(email, password)
    # user_token = user_login_credentials['token']   

    return {
        'u_id': user_id,
        'token': user_login_credentials['token']  
    }

def check_if_valid_email(email):
    # makig a check existing email and duplicate email function is same just different
    # returns, instead implemnt it a bit differently when calling can solve the 
    # purpose with only one function
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    return False

def check_if_valid_password(password):
    allowed_special_symbols =['!', '@', '#', '$', '%', '^', '&', '*']   

    if not 6 <= len(password) <= 32:
        return False

    if not any(character.isdigit() for character in password): 
        return False 
          
    if not any(character.isupper() for character in password): 
        return False
          
    if not any(character.islower() for character in password): 
        return False
          
    if not any(character in allowed_special_symbols for character in password): 
        return False

    return True          

def check_name_length(name_to_check):
    if not 1 <= len(name_to_check) <= 50:
        return False
    return True

def check_if_registered_user(email):
    for user in data.data['users']:
        if user['email'] == email:
            return True
    return False

def get_user_id(email):
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
    concatenated_names = name_first + name_last
    handle_str = concatenated_names[:20]
    return handle_str

def check_password(email, password):
    for user in data.data['users']:
        if user['email']  == email:
            if user['password'] == password:
                return True
    return False

def check_token(token):
    for user in data.data['users']:
        if user['token'] == token:
            return True
    return False

# later make this as store_And_generate_token(email):, i.e. this will generate 
# token, store it and then return it
def store_generated_token(email, user_token):
    for user in data.data['users']:
            if user['email']  == email:
                user['token'] = user_token

# or do it this way, find the user with matching token and relace the token with invalid token string
def invalidating_token(token):
    for user in data.data['users']:
        if user['token']  == token:
            user['token'] = 'invalid_token'
            return True
    return False
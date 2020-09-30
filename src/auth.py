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
    if None in {email, password}:
        raise InputError('Insufficient parameters. Please enter: email, password.')

    if not check_if_valid_email(email):
         raise InputError('Please enter a valid email-id.') 

    if not check_if_registered_user(email):
        raise InputError('Please register since you are not registered yet.')

    if not check_password(email, password):
        raise InputError('Please enter the correct password.') 

    # since no errors, all is good now, gnerate a token and get u_id
    user_id = get_user_id(email)
    user_token = email
    store_generated_token(email, user_token)

    # IMPORTANT : Tell everyone i've implemented email as token as of now, rather 
    # than name_first + name_last, just aviding extra code since this a temp fix,
    # hence change data.py
    # CHANGE MY TOKEN TEST(s)

    return {
        'u_id': user_id,
        'token': user_token
    }

def auth_logout(token):
    if None in {token}:
        raise InputError('Insufficient parameters. Please enter: token')
    
    status = False

    if check_token(token) is False:
        return {
            'is_success': status
        }

    # now find u_id and then put a invalid token in place, maybe sjust have a common invalid token for identification
    # modufy get_user_id function such that the parameter passed can either be email or token and if returns u_id, IMPORTANT

    # or do it this way, find the user with matching token and relace the token with invalid token string
    for user in data.data['users']:
        if user['token']  == token:
            user['token'] = 'invalid_token'
            status = True

    return {
        'is_success': status
    }

def auth_register(email, password, name_first, name_last):
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

    if check_if_registered_user(email):
        raise InputError('Email address is already being used by another user')
    
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
        if user['email']  == email:
            user_id = user['u_id']
            return user_id
        user_count += 1 # this is for register function, i.e. we need to make user id there, then it is retunr user_count + 1
    return user_count + 1
    # add a general retunr here, think

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

def store_generated_token(email, user_token):
    for user in data.data['users']:
            if user['email']  == email:
                user['token'] = user_token
                
# not needed right now
# def generate_token():
#     pass
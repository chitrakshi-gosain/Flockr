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
    return {
        'u_id': 1,
        'token': '12345',
    }

def check_if_valid_email():
    pass

def check_if_registered_user():
    pass

def match_password():
    pass

def check_password():
    pass

def check_if_existing_user():
    pass

def check_name_length():
    pass
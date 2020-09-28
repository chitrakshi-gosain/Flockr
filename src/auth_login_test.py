# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain
# Reviewer - Ahmet K

# Iteration 1
'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_AVAILABLE_FOR_THE_TEST(PARAMETERS) return (RETURN_TYPE):
-> auth_register(email, password, name_first, name_last) return (u_id, token)
-> auth_login(email,password) return (u_id, token)
-> auth_logout(token) return (is_sucess)
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

import auth
import pytest

def test_successful_login():
    pass

def test_invalid_email():
    pass

def test_unregistered_user():
    pass

def test_wrong_password():
    pass

def test_re_login():
    pass

def test_add_more_later():
    pass
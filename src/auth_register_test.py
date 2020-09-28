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
-> email is already being used by another user
-> password is less than 6 characters
-> name_first is not between 1 and 50 characters
-> name_last is not between 1 and 50 characters
# for name check make a check_length function and send parameters to it during test
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> user can be already logged-in and trying to re-log-in, this has two 
   possibilties:
        *log-in to self account again
        *log-in to someone else's account
   however, in both cases user should be asked to logout first and then try   
'''

import auth
import pytest

def test_trying_to_login():
    pass

def test_invalid_email():
    pass

def test_existing_email_registeration():
    pass

def test_too_long_first_name():
    pass

def test_too_long_last_name():
    pass

def test_too_short_password():
    pass
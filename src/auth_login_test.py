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
   possibilties, confirm if this should be considered yet:
        *log-in to self account again
        *log-in to someone else's account
   however, in both cases user should be asked to logout first and then try
-> do we keep track of passwords? if in case user enters old password, then??
'''

import auth
import pytest
from error import InputError

def test_successful_login():
    auth.auth_register('validemailid0@gmail.com', '123Abc!', 'Valid', 'User')
    auth.auth_login('validemail0@gmail.com', '123Abc!')

def test_invalid_email():
    with pytest.raises(InputError):
        auth.auth_register('validemailid_gmail.com', '123Abc!', 'Valid', 'User')

def test_unregistered_user():
    with pytest.raises(InputError):
        auth.auth_login('notvalidemail1@gmail.com', '123Abc!')

def test_wrong_password():
    auth.auth_register('validemailid2@gmail.com', '123Abc!', 'Valid', 'User')
    auth.auth_login('validemail2@gmail.com', 'cbA321!')

def test_re_login():
    # not sure if it is to be implemented in iteration 1 or at all
    pass

def test_insufficient_parameters():
    with pytest.raises(InputError):
        auth.auth_login('notvalidemail1@gmail.com', None)
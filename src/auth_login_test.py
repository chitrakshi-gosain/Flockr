# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain
# Reviewer - Ahmet K

# Iteration 1
'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_USED_FOR_THE_TEST(PARAMETERS) return (RETURN_TYPE):
-> auth_register(email, password, name_first, name_last) return (u_id, token)
-> auth_login(email,password) return (u_id, token)
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
from user import user_profile

def test_successful_login_with_everything_valid():
    # modify this as in check if token is valid, do it after making function, probs
    # will have to user.py for this and dat.py too, have a basic idea of what to do
    # this is a stub atm
    auth.auth_register('logintestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    test_user_with_valid_token = auth.auth_login('logintestvalidemailid0@gmail.com', '123Abc!0')
    # can work further if we makes changes to dat for easy extraction of stuff
    # or think some other way if we dont change data
    # but it's a black box test, should i depend on data.py this much???
    assert(test_user_with_valid_token) == 'a' # totally unncessary, just to  avoid error of unused variable
    pass

def test_invalid_email():
    with pytest.raises(InputError):
        auth.auth_login('logintestinvalidemailid_gmail.com', '123Abc!!')

def test_unregistered_user():
    auth.auth_register('logintestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    with pytest.raises(InputError):
        auth.auth_login('unregisteredemail1@gmail.com', '123Abc!!')

def test_wrong_password():
    auth.auth_register('logintestvalidemailid2@gmail.com', '123Abc!2', 'Valid', 'User2')
    auth.auth_login('logintestvalidemailid2@gmail.com', 'cbA321!!')

def test_re_login():
    auth.auth_register('logintestvalidemailid3@gmail.com', '123Abc!3', 'Valid', 'User3')
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid3@gmail.com', '123Abc!3')

def test_insufficient_parameters():
    auth.auth_register('logintestvalidemailid4@gmail.com', '123Abc!4', 'Valid', 'User4')
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid4@gmail.com', None)

'''
NOTES:
# eliminate the auth.auth_register in each test and maybe just have it once at top, will it work?
# discuss and add a test for return_type of function, probs
'''
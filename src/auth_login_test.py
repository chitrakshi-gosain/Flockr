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
-> allow multiple logins
-> do we keep track of passwords? if in case user enters old password, then??, 
   ask Hayden if this needs to be done
'''

import auth
import pytest
from other import clear
from error import InputError
from user import user_profile

def test_successful_login_with_everything_valid():
    clear()
    auth.auth_register('logintestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    auth.auth_login('logintestvalidemailid0@gmail.com', '123Abc!0')
    # is this ok?

def test_invalid_email():
    clear()
    auth.auth_register('logintestinvalidemailid@gmail.com', '123Abc!!', 'Valid', 'User!')
    with pytest.raises(InputError):
        auth.auth_login('logintestinvalidemailid_gmail.com', '123Abc!!')

def test_unregistered_user():
    clear()
    auth.auth_register('logintestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    with pytest.raises(InputError):
        auth.auth_login('unregisteredemail1@gmail.com', '123Abc!!')

def test_wrong_password():
    clear()
    auth.auth_register('logintestvalidemailid2@gmail.com', '123Abc!2', 'Valid', 'User2')
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid2@gmail.com', 'cbA321!!')

def test_insufficient_parameters():
    clear()
    auth.auth_register('logintestvalidemailid3@gmail.com', '123Abc!3', 'Valid', 'User3')
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid3@gmail.com', None)

def test_return_type():
    clear()
    auth.auth_register('registerationtestvalidemailid4@gmail.com', '123Abc!4', 'Valid', 'User4')
    test_user_4_login_credentials = auth.auth_login('registerationtestvalidemailid4@gmail.com', '123Abc!4')
    assert isinstance(test_user_4_login_credentials['u_id'], int)
    assert isinstance(test_user_4_login_credentials['token'], str) 

# altho register calls login, there is still 1% chance that u_id and token returned from login function might be played with.
def test_login_u_id():
    clear()
    test_user_5_register_credentials = auth.auth_register('registerationtestvalidemailid5@gmail.com', '123Abc!5', 'Valid', 'User5')
    test_user_5_login_credentials = auth.auth_login('registerationtestvalidemailid5@gmail.com', '123Abc!5')
    assert test_user_5_login_credentials['u_id'] == test_user_5_register_credentials['u_id']

def test_login_unique_token_and_u_id():
    clear()
    auth.auth_register('registerationtestvalidemailid6@gmail.com', '123Abc!6', 'Valid', 'User6')
    test_user_6_login_credentials = auth.auth_login('registerationtestvalidemailid6@gmail.com', '123Abc!6')
    auth.auth_register('registerationtestvalidemailid7@gmail.com', '123Abc!7', 'Valid', 'User7')
    test_user_7_login_credentials = auth.auth_login('registerationtestvalidemailid7@gmail.com', '123Abc!7')

    assert test_user_6_login_credentials != test_user_7_login_credentials

    tokens = [test_user_6_login_credentials['token'], test_user_7_login_credentials['token']]
    assert len(set(tokens)) == len(tokens)

def test_multiple_logins():
    clear()
    auth.auth_register('registerationtestvalidemailid8@gmail.com', '123Abc!8', 'Valid', 'User8')
    auth.auth_login('registerationtestvalidemailid8@gmail.com', '123Abc!8')
    auth.auth_login('registerationtestvalidemailid8@gmail.com', '123Abc!8')
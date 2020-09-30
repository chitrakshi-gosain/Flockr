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
-> auth_logout(token) return (is_sucess)
'''

'''
EXCEPTIONS
Error type: AccessError
-> token passed is not a valid token
'''

'''
KEEP IN MIND:
-> check if user is logged in before logging out
-> check if token was invaildated, maybe just make a function to check that in sense make a dictionary for valid tokens with uid somehwere
'''

import auth
import pytest
from other import clear
from user import user_profile
from error import AccessError, InputError

def test_successful_logout():
    clear()
    auth.auth_register('logouttestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    test_user_0 = auth.auth_login('logouttestvalidemailid0@gmail.com', '123Abc!0')
    assert auth.auth_logout(test_user_0['token'])

def test_active_token_now_invalid():
    clear()
    auth.auth_register('logouttestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    test_user_1 = auth.auth_login('logouttestvalidemailid1@gmail.com', '123Abc!1')
    assert auth.auth_logout(test_user_1['token'])
    with pytest.raises(AccessError):
        auth.auth_logout('invalid_token')

def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        auth.auth_logout(None)
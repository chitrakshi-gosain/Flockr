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
Error type: AccessError
-> token passed is not a valid token
'''

'''
KEEP IN MIND:
-> check if user is logged in before logging out
-> check if token was invaildated, maybe just make a function to check that 
-> check if token is valid before klogout
-> check is token is no onger valid after logout - sense wise it's same as first one
'''

import auth
import pytest

def test_successful_logout():
    pass

def test_active_token_now_invalid():
    pass
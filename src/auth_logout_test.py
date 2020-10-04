# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_sucess}
'''

'''
EXCEPTIONS
Error type: AccessError
-> token passed is not a valid token
'''

'''
KEEP IN MIND:
-> check if user is logged in before logging out
-> check if token was invaildated, if invalid token is passed raise AccessError
'''

import auth
import pytest
from other import clear
from user import user_profile
from error import AccessError, InputError

def test_successful_logout():
    '''
    Tests that auth_logout returns True on successful logout
    '''

    clear()
    test_user_0 = auth.auth_register('logouttestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    assert auth.auth_logout(test_user_0['token']) == {'is_success' : True}

def test_active_token_now_invalid():
    '''
    Tests that auth_logout returns True on successful logout the first time, 
    but second time when the same token is passed it raises an AccessError
    '''

    clear()
    auth.auth_register('logouttestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    test_user_1 = auth.auth_login('logouttestvalidemailid1@gmail.com', '123Abc!1')
    assert auth.auth_logout(test_user_1['token']) == {'is_success' : True}
    with pytest.raises(AccessError):
        auth.auth_logout(test_user_1['token'])

def test_invalid_token():
    '''
    Tests that auth_logout raises an AccessError when an invalid token is passed
    '''

    clear()
    with pytest.raises(AccessError):
        auth.auth_logout('invalid_token')

def test_whitespace_as_token():
    '''
    Tests that auth_logout raises an AccessError when a whitespace is passed 
    as token
    '''

    clear()
    with pytest.raises(AccessError):
        auth.auth_logout(' ')

def test_insufficient_parameters():
    '''
    Tests that auth_logout raises an InputError when less than expected  
    parameters are passed
    '''

    clear()
    with pytest.raises(InputError):
        auth.auth_logout(None)

def test_return_type():
    '''
    Tests that auth_logout returns the expected datatype i.e. 
    { is_success : boolean }
    '''

    clear()
    test_user_2_registeration_credentials =  auth.auth_register('logouttestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User2')
    test_user_2_logout_status = auth.auth_logout(test_user_2_registeration_credentials['token'])
    assert isinstance(test_user_2_logout_status, dict)
    assert isinstance(test_user_2_logout_status['is_success'], bool)
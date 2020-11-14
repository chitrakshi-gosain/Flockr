'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import time
import pytest
from error import InputError
from auth import auth_login, auth_logout

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> email entered is not a valid email
    -> email entered does not belong to a user
    -> password is not correct
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> allow multiple logins
-> do we keep track of passwords? if in case user enters old password,
   then??, ask Hayden if this needs to be done
'''

def test_successful_login_with_everything_valid(initialise_user_data):
    '''
    Tests that auth_login logs the user in successfully
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    auth_login('user0@email.com', 'user0_pass1!')

def test_invalid_email(reset):
    '''
    Tests that auth_login raises an InputError when an invalid email-id
    is passed as one of the parameters
    '''

    with pytest.raises(InputError):
        auth_login('user0_email.com', 'user0_pass1!')

def test_unregistered_user(reset):
    '''
    Tests that auth_login raises an InputError when an unregistered user
    tries to log-in
    '''

    with pytest.raises(InputError):
        auth_login('user00@email.com', 'user0_pass1!')

def test_wrong_password(initialise_user_data):
    '''
    Tests that auth_login raises an InputError when a wrong password is
    passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    with pytest.raises(InputError):
        auth_login('user0@email.com', 'user0_Pass1!')

def test_return_type(initialise_user_data):
    '''
    Tests that auth_login returns the expected datatype i.e.
    {u_id : int, token : str}
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')

    assert isinstance(test_user_0_login, dict)
    assert isinstance(test_user_0_login['u_id'], int)
    assert isinstance(test_user_0_login['token'], str)

def test_login_u_id(initialise_user_data):
    '''
    Tests that auth_register and auth_login return same values of token
    and u_id, as there may be a slightest possibility that token or u_id
    of the user might be played around with
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    assert test_user_0_login['u_id'] == test_user_0['u_id']

def test_login_unique_token_and_u_id(initialise_user_data):
    '''
    Tests that auth_login returns a unique u_id and token for each user
    '''

    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    test_user_1_login = auth_login('user1@email.com', 'user1_pass1!')

    assert test_user_0_login != test_user_1_login

    tokens = [test_user_0_login['token'], test_user_1_login['token']]
    assert len(set(tokens)) == len(tokens)

def test_looking_for_negative_u_id(initialise_user_data):
    '''
    Tests that auth_login does not return a negative u_id for a user
    '''

    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    assert test_user_0_login['u_id'] >= 0

def test_non_ascii_password(initialise_user_data):
    '''
    Tests that auth_login does not accept a Non-ASCII password as one
    the parameters passed to it
    '''

    with pytest.raises(InputError):
        auth_login('user0@email.com', 'user0 \n pass1!')

def test_multiple_login_different_token(initialise_user_data):
    '''
    Tests that auth_login allows multiple logins, and each login session
    has a unique token
    '''

    test_user_0_login0 = auth_login('user0@email.com', 'user0_pass1!')
    time.sleep(5)
    test_user_0_login1 = auth_login('user0@email.com', 'user0_pass1!')

    assert test_user_0_login0 != test_user_0_login1

    tokens = [test_user_0_login0['token'], test_user_0_login1['token']]
    assert len(set(tokens)) == len(tokens)
    
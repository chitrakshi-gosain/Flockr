'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 3
'''

import pytest
from error import InputError
from auth import auth_passwordreset_request, auth_passwordreset_reset

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_passwordreset_request(email) return {}
-> auth_passwordreset_reset(reset_code, new_password) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> reset_code is not a valid reset_code
    -> password entered is not a valid password
    -> password entered is similar to one of the old passwords
'''

def test_invalid_reset_code(reset):
    '''
    Tests that auth_passwordreset_reset raises an AccessError when an
    invalid reset code is passed as one of the parameters
    '''

    with pytest.raises(InputError):
        auth_passwordreset_reset(' ', 'some_password')

def test_new_password_too_short(initialise_user_data):
    '''
    Tests that auth_passwordreset_reset raises an InputError when new
    password is less than 6 characters long
    '''
    
    reset_code = auth_passwordreset_request('user0@email.com')
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, 'some')

def test_new_password_too_long(initialise_user_data):
    '''
    Tests that auth_passwordreset_reset raises an InputError when new
    password is more than 32 characters long
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, 'some' * 10)

def test_successful_reset(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    auth_passwordreset_reset(reset_code, 'user0_password1!')

def test_return_type(initialise_user_data):
    '''
    Tests that auth_passwordreset_reset returns the expected datatype
    i.e. {}
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    assert not auth_passwordreset_reset(reset_code, 'user0_password1!')

def test_new_password_is_actually_old(initialise_user_data):
    '''
    Tests that auth_passwordreset_reset raises an error when old
    password is entered as new password while resetting
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, 'user0_pass1!')

def test_new_password_is_one_of_old_ones(initialise_user_data):
    '''
    Tests that auth_passwordreset_reset raises an error when one of the
    old passwords is entered as new password while resetting
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    assert not auth_passwordreset_reset(reset_code, 'user0_password1!')

    reset_code = auth_passwordreset_request('user0@email.com')
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, 'user0_pass1!')

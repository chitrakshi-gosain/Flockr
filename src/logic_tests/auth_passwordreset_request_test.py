'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 3
'''

import pytest
from error import InputError
from auth import auth_passwordreset_request

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_passwordreset_request(email) return {}
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
'''

def test_invalid_email(reset):
    '''
    Tests that auth_passwordreset_request raises an InputError when an
    invalid email-id is passed as one of the parameters
    '''

    with pytest.raises(InputError):
        auth_passwordreset_request('user0_email.com')

def test_unregistered_user(reset):
    '''
    Tests that auth_passwordreset_request raises an InputError when an
    unregistered user tries to request for a reset code to change his
    password
    '''

    with pytest.raises(InputError):
        auth_passwordreset_request('user00@email.com')

def test_return_type(initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully returns the reset
    code which is of string type as per the spec
    '''

    reset_code = auth_passwordreset_request('user0@email.com')
    assert isinstance(reset_code, str)

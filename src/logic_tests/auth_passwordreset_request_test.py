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
    -> email entered is not a valid email
    -> email entered does not belong to a user
'''

'''
KEEP IN MIND:
-> ...
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
    unregistered user tries to log-in
    '''

    with pytest.raises(InputError):
        auth_passwordreset_request('user00@email.com')

def test_reset_code_sent_succesfully(initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully send an email to
    the user with reset code so that he can reset his password
    '''

    auth_passwordreset_request('user0@email.com')
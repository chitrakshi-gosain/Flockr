'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import pytest
from other import clear
from error import AccessError, InputError
from auth import auth_login, auth_logout, auth_register

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
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
-> check if user is logged in before logging out
-> check if token was invaildated, if invalid token is passed raise
   AccessError
'''

@pytest.fixture
def reset():
    '''
    Resets the internal data of the application to it's initial state
    '''

    clear()

@pytest.fixture
def initialise_user_data(reset):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    user0_details = auth_register('user0@email.com', 'user0_pass1!', \
                                 'user0_first', 'user0_last')

    return {
        'user0': user0_details
    }

def test_successful_logout(initialise_user_data):
    '''
    Tests that auth_logout returns True on successful logout
    '''

    test_user_0 = initialise_user_data['user0']
    assert auth_logout(test_user_0['token'])

def test_active_token_now_invalid(initialise_user_data):
    '''
    Tests that auth_logout returns True on successful logout the first
    time, but second time when the same token is passed it raises an
    AccessError
    '''

    test_user_0_login = initialise_user_data['user0']
    assert auth_logout(test_user_0_login['token'])
    with pytest.raises(AccessError):
        auth_logout(test_user_0_login['token'])

def test_invalid_token(initialise_user_data):
    '''
    Tests that auth_logout raises an AccessError when an invalid token
    is passed as one of the parameters
    '''

    with pytest.raises(AccessError):
        auth_logout('invalid_token')

def test_whitespace_as_token(initialise_user_data):
    '''
    Tests that auth_logout raises an AccessError when a whitespace is
    passed as token
    '''

    with pytest.raises(AccessError):
        auth_logout(' ')

def test_return_type(initialise_user_data):
    '''
    Tests that auth_logout returns the expected datatype i.e.
    { is_success : boolean }
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_logout_status = auth_logout(test_user_0['token'])
    assert isinstance(test_user_0_logout_status, dict)
    assert isinstance(test_user_0_logout_status['is_success'], bool)

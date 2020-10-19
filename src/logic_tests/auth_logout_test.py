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
Error type: InputError
    -> insufficient parameters
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
def initialise_user_data():
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent

    '''

    user0_details = auth_register('user0@email.com', 'user0_pass1!', \
                                 'user0_first', 'user0_last')

    return {
        'user0': user0_details
    }

def test_successful_logout(reset, initialise_user_data):
    '''
    Tests that auth_logout returns True on successful logout
    '''

    test_user_0 = initialise_user_data['user0']
    assert auth_logout(test_user_0['token'])

def test_active_token_now_invalid(reset, initialise_user_data):
    '''
    Tests that auth_logout returns True on successful logout the first
    time, but second time when the same token is passed it raises an
    AccessError
    '''

    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    assert auth_logout(test_user_0_login['token'])
    with pytest.raises(AccessError):
        auth_logout(test_user_0_login['token'])

def test_invalid_token(reset, initialise_user_data):
    '''
    Tests that auth_logout raises an AccessError when an invalid token
    is passed as one of the parameters
    '''

    with pytest.raises(AccessError):
        auth_logout('invalid_token')

def test_whitespace_as_token(reset, initialise_user_data):
    '''
    Tests that auth_logout raises an AccessError when a whitespace is
    passed as token
    '''

    with pytest.raises(AccessError):
        auth_logout(' ')

def test_insufficient_parameters(reset, initialise_user_data):
    '''
    Tests that auth_logout raises an InputError when less than expected
    parameters are passed
    '''

    with pytest.raises(InputError):
        auth_logout(None)

def test_return_type(reset, initialise_user_data):
    '''
    Tests that auth_logout returns the expected datatype i.e.
    { is_success : boolean }
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_logout_status = auth_logout(test_user_0['token'])
    assert isinstance(test_user_0_logout_status, dict)
    assert isinstance(test_user_0_logout_status['is_success'], bool)

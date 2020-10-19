'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import pytest
from other import clear
from error import InputError
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
    user1_details = auth_register('user1@email.com', 'user1_pass1!', \
                                 'user1_first', 'user1_last')

    return {
        'user0': user0_details,
        'user1': user1_details
    }

def test_successful_login_with_everything_valid(reset, initialise_user_data):
    '''
    Tests that auth_login logs the user in successfully
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    auth_login('user0@email.com', 'user0_pass1!')

def test_invalid_email(reset, initialise_user_data):
    '''
    Tests that auth_login raises an InputError when an invalid email-id
    is passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    with pytest.raises(InputError):
        auth_login('user0_email.com', 'user0_pass1!')

def test_unregistered_user(reset, initialise_user_data):
    '''
    Tests that auth_login raises an InputError when an unregistered user
    tries to log-in
    '''

    with pytest.raises(InputError):
        auth_login('user00@email.com', 'user0_pass1!')

def test_wrong_password(reset, initialise_user_data):
    '''
    Tests that auth_login raises an InputError when a wrong password is
    passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    with pytest.raises(InputError):
        auth_login('user0@email.com', 'user0_Pass1!')

def test_insufficient_parameters(reset, initialise_user_data):
    '''
    Tests that auth_login raises an InputError when less than expected
    parameters are passed
    '''

    test_user_0 = initialise_user_data['user0']
    auth_logout(test_user_0['token'])
    with pytest.raises(InputError):
        auth_login('user0@email.com', None)

def test_return_type(reset, initialise_user_data):
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

def test_login_u_id(reset, initialise_user_data):
    '''
    Tests that auth_register and auth_login return same values of token
    and u_id, as there may be a slightest possibility that token or u_id
    of the user might be played around with
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    assert test_user_0_login['u_id'] == test_user_0['u_id']

def test_login_unique_token_and_u_id(reset, initialise_user_data):
    '''
    Tests that auth_login returns a unique u_id and token for each user
    '''

    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    test_user_1_login = auth_login('user1@email.com', 'user1_pass1!')

    assert test_user_0_login != test_user_1_login

    tokens = [test_user_0_login['token'], test_user_1_login['token']]
    assert len(set(tokens)) == len(tokens)

# later modify this to check each login from multiple logins has
# different token
def test_multiple_logins(reset, initialise_user_data):
    '''
    Tests that auth_login allows multiple logins
    '''

    auth_login('user0@email.com', 'user0_pass1!')
    auth_login('user0@email.com', 'user0_pass1!')
    auth_login('user0@email.com', 'user0_pass1!')

def test_looking_for_negative_u_id(reset, initialise_user_data):
    '''
    Tests that auth_login does not return a negative u_id for a user
    '''

    test_user_0_login = auth_login('user0@email.com', 'user0_pass1!')
    assert test_user_0_login['u_id'] >= 0

def test_non_ascii_password(reset, initialise_user_data):
    '''
    Tests that auth_login does not accept a Non-ASCII password as one
    the parameters passed to it
    '''

    with pytest.raises(InputError):
        auth_login('user0@email.com', 'user0 \n pass1!')

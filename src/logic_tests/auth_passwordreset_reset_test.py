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
'''

'''
KEEP IN MIND:
-> ...
'''

def test_invalid_reset_code(reset):
    '''
    ADD DOCSTRING HERE
    '''

    with pytest.raises(InputError):
        auth_passwordreset_reset(' ', 'some_password')

def test_new_password_too_short(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    with pytest.raises(InputError):
        auth_passwordreset_reset('reset_code', 'some')

def test_new_password_too_long(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    with pytest.raises(InputError):
        auth_passwordreset_reset('reset_code', 'some' * 10)

# THESE MAKE NO SENSE AT ALL BECAUSE NO EMAIL IS SENT FROM REQUEST FUNCTION, CONFIRM BUT, WILL BE COVERED IN HTTP TEST ANYWAY
# def test_new_password_is_actually_old(initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     auth_passwordreset_request('user0@email.com')
#     with pytest.raises(InputError):
#         auth_passwordreset_reset('reset_code', 'user0_pass1!')

# def test_successful_reset(initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     auth_passwordreset_request('user0@email.com')
#     auth_passwordreset_reset('reset_code', 'user0_password1!')

# def test_return_type(initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     auth_passwordreset_request('user0@email.com')
#     assert not auth_passwordreset_reset('reset_code', 'user0_password1!')

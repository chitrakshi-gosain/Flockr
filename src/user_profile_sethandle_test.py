'''
Created collaboratively by Wed15Team2 2020 T3
Contributer - Chitrakshi Gosain

Iteration 2
'''

import pytest
from other import clear
from error import InputError, AccessError
from user import user_profile, user_profile_sethandle
from auth import auth_register

# edit basic template to fit this file

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
-> user_profile_sethandle(toke, handle_str) return {}
'''

'''
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> handle_str must be between 3 and 20 characters
    -> handle is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
-> i have some assumptions testing in test, add them to assumptions.md
'''

def test_insufficient_parameters():
    '''
    ADD DOCTSRING HERE
    '''

    clear()
    with pytest.raises(InputError):
        user_profile_sethandle(None, None)

def test_return_type():
    '''
    ADD DOCSTRING HERE
    '''

    clear()
    test_user_0_register = auth_register('myemailid0@gmail.com', '123Abc!0', \
                                        'Valid', 'User0')
    test_user_0_updatedhandle = user_profile_sethandle(test_user_0_register['token'], \
                                       'mynewhandle')
    assert isinstance(test_user_0_updatedhandle, dict)
    dict_is_empty = not test_user_0_updatedhandle
    assert dict_is_empty

def test_invalid_token():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_too_short_handle_str():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_too_long_handle_str():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_succesful_handle_updatation():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_handle_3_chars():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_handle_20_chars():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_non_ascii_handle():
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that handles can have non ascii chars
    '''

    clear()

def test_existing_handle():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_whitespace_handle():
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that only white space cant be valid handle
    '''

    clear()
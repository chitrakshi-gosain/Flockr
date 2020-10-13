'''
Created collaboratively by Wed15Team2 2020 T3
Contributer - Chitrakshi Gosain

Iteration 2
'''

import pytest
from other import clear
from error import InputError, AccessError
from user import user_profile, user_profile_setemail
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
    -> email entered is not a valid email
    -> email address is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
'''

def test_insufficient_parameters():
    '''
    ADD DOCTSRING HERE
    '''

    clear()
    with pytest.raises(InputError):
        user_profile_setemail(None, None)

def test_return_type():
    '''
    ADD DOCSTRING HERE
    '''

    clear()
    test_user_0_register = auth_register('myemailid0@gmail.com', '123Abc!0', \
                                        'Valid', 'User0')
    test_user_0_updatedemail = user_profile_setemail(test_user_0_register['token'], \
                                       'mynewemail0@gmail.com')
    assert isinstance(test_user_0_updatedemail, dict)
    # checking if returned is empty, may or may not work 3 this line is
    # dic_is_empty == True, but pythonic
    dict_is_empty = not test_user_0_updatedemail
    assert dict_is_empty

def test_invalid_token():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_invalid_email():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_existing_email():
    '''
    ADD DOCSTRING HERE
    # not unique email
    '''

    clear()

def test_succesful_email_updatation():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

def test_only_unique_changes_accepted():
    '''
    ADD DOCSTRING HERE
    # reguister two users, then change emails of both, but unique and everything should be successful
    '''

    clear()

'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Joseph Knox

Iteration 2
'''

import pytest
import auth
from user import user_profile, user_profile_setname
from error import InputError, AccessError
from other import clear

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
'''

'''
EXCEPTIONS
Error type: InputError
    -> name_first is not between 1 and 50 characters inclusively in length
    -> name_last is not between 1 and 50 characters inclusively in length
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_user_profile_setname_no_errors():
    '''
    basic test with no edge case or errors raised
    '''
    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    name_first_new = 'name_first_new'
    name_last_new = 'name_last_new'

    user_profile_setname(token, name_first_new, name_last_new)

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_new
    assert user_dict['name_last'] == name_last_new

def test_user_profile_setname_firstname_tooshort():
    '''
    test that user_profile_setname raises InputError
    if provided name_first is <1 characters in length
    '''
    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    # new name_first <1 characters in length
    name_first_new = ''
    name_last_new = 'name_last_new'

    with pytest.raises(InputError):
        user_profile_setname(token, name_first_new, name_last_new)

def test_user_profile_setname_firstname_toolong():
    '''
    test that user_profile_setname raises InputError
    if provided name_first is >50 characters in length
    '''
    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    # new name_first >50 characters in length
    name_first_new = '123456789012345678901234567890123456789012345678901'
    name_last_new = 'name_last_new'

    with pytest.raises(InputError):
        user_profile_setname(token, name_first_new, name_last_new)

def test_user_profile_setname_lastname_tooshort():
    '''
    test that user_profile_setname raises InputError
    if provided name_last is <1 characters in length
    '''
    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    # new name_last <1 characters in length
    name_first_new = 'name_first_new'
    name_last_new = ''

    with pytest.raises(InputError):
        user_profile_setname(token, name_first_new, name_last_new)

def test_user_profile_setname_lastname_toolong():
    '''
    test that user_profile_setname raises InputError
    if provided name_last is >50 characters in length
    '''
    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    # new name_last >50 characters in length
    name_first_new = 'name_first_new'
    name_last_new = '123456789012345678901234567890123456789012345678901'

    with pytest.raises(InputError):
        user_profile_setname(token, name_first_new, name_last_new)

def test_user_profile_setname_accesserror():
    '''
    test that user_profile_setname raises AccessError
    if provided token is invalid
    '''

    clear()

    name_first_old = 'name_first_old'
    name_last_old = 'name_last_old'

    user_details = auth.auth_register("user@email.com", "user_pass",
                                      "name_first_old", "name_last_old")
    token = user_details['token']
    u_id = user_details['u_id']

    user_profile_info = user_profile(token, u_id)
    user_dict = user_profile_info["user"]

    assert user_dict['name_first'] == name_first_old
    assert user_dict['name_last'] == name_last_old

    # new name_last >50 characters in length
    name_first_new = 'name_first_new'
    name_last_new = 'name_last_new'

    with pytest.raises(AccessError):
        user_profile_setname(' ', name_first_new, name_last_new)

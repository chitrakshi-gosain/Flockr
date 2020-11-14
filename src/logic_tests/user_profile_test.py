'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import pytest
from auth import auth_logout
from user import user_profile
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> user with u_id is not a valid_user
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_user_profile_valid_own(initialise_user_data):
    '''
    Testing users checking their own profiles
    '''
    user_data = initialise_user_data

    profile_data = user_profile(user_data['owner']['token'], user_data['owner']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['owner']['u_id'],
            'email': 'owner@email.com',
            'name_first': 'owner_first',
            'name_last': 'owner_last',
            'handle_str': 'owner_firstowner_las',
            'profile_img_url': '',
        }
    }

    assert profile_data == exp_dict

    profile_data = user_profile(user_data['user0']['token'], user_data['user0']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['user0']['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las',
            'profile_img_url': '',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_else(initialise_user_data):
    '''
    Testing users checking other user's profiles
    '''
    user_data = initialise_user_data

    profile_data = user_profile(user_data['user0']['token'], user_data['user1']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['user1']['u_id'],
            'email': 'user1@email.com',
            'name_first': 'user1_first',
            'name_last': 'user1_last',
            'handle_str': 'user1_firstuser1_las',
            'profile_img_url': '',
        },
    }

    assert profile_data == exp_dict

    profile_data = user_profile(user_data['user1']['token'], user_data['admin']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['admin']['u_id'],
            'email': 'admin@email.com',
            'name_first': 'admin_first',
            'name_last': 'admin_last',
            'handle_str': 'admin_firstadmin_las',
            'profile_img_url': '',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_logout(initialise_user_data):
    '''
    Testing the retrieval of profile data from a user that is logged out
    by a user that is logged in
    '''

    user_data = initialise_user_data

    auth_logout(user_data['user0']['token'])

    profile_data = user_profile(user_data['user1']['token'], user_data['user0']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['user0']['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las',
            'profile_img_url': '',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_invalid_uid(initialise_user_data):
    '''
    Testing user_profile with an invalid u_id parameter
    '''

    invalid_uid = -1

    with pytest.raises(InputError):
        user_profile(initialise_user_data['user0']['token'], invalid_uid)

def test_user_profile_invalid_token(initialise_user_data):
    '''
    Testing user_profile with an invalid token parameter
    '''

    user_data = initialise_user_data

    invalid_token = user_data['user0']['token']
    auth_logout(user_data['user0']['token'])

    with pytest.raises(AccessError):
        user_profile(invalid_token, user_data['user1']['u_id'])

'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import pytest
from auth import auth_logout
from other import users_all
from error import AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> users_all(token) return {users}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS:
AccessError
-> Invalid token
'''

def test_users_all_basic(initialise_user_data):
    '''
    Basic valid test case of users_all
    '''

    user_data = initialise_user_data

    all_users = users_all(user_data['admin']['token'])

    exp_dict = {
        'users': [
            {
                'u_id': user_data['admin']['u_id'],
                'email': 'admin@email.com',
                'name_first': 'admin_first',
                'name_last': 'admin_last',
                'handle_str': 'admin_firstadmin_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
                'profile_img_url': '',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_logout(initialise_user_data):
    '''
    Tests that all user profiles are returned even if
    some users are logged out
    '''

    user_data = initialise_user_data

    auth_logout(user_data['owner']['token'])
    auth_logout(user_data['user3']['token'])

    all_users = users_all(user_data['admin']['token'])

    exp_dict = {
        'users': [
            {
                'u_id': user_data['admin']['u_id'],
                'email': 'admin@email.com',
                'name_first': 'admin_first',
                'name_last': 'admin_last',
                'handle_str': 'admin_firstadmin_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
                'profile_img_url': '',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_invalid_token(initialise_user_data):
    '''
    Testing users_all with an invalid token parameter
    '''

    invalid_token = initialise_user_data['admin']['token']
    auth_logout(initialise_user_data['admin']['token'])

    with pytest.raises(AccessError):
        users_all(invalid_token)

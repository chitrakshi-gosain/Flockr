'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import pytest
from auth import auth_register, auth_logout
from other import clear, users_all
from error import AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> users_all(token) return {users}
'''

'''
@pytest.fixture
def user_data():
    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John',\
                                'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', \
                                'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', \
                                'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', \
                                  'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df',\
                                  'Donald', 'Richards')

    # Returns user data that is implementation dependent (id, token)
    return {
        'john': john_details, admin
        'jane': jane_details, user0
        'noah': noah_details, user1
        'ingrid': ingrid_details, user2
        'donald': donald_details user3
    }
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
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
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
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
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

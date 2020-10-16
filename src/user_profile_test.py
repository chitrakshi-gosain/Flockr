'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import pytest
from auth import auth_register, auth_logout
from user import user_profile
from other import clear
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

@pytest.fixture
def user_data():
    '''
    Sets up various user sample data for testing purposes
    '''

    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Descriptive test data
    owner_details = auth_register('owner@email.com', 'Owner_pass1!', 'owner_first', 'owner_last')
    user1_details = auth_register('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    user2_details = auth_register('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    user3_details = auth_register('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    user4_details = auth_register('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
    user5_details = auth_register('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John', 'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', 'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', 'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', 'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df', 'Donald', 'Richards')

    # Returns user data that is implementation dependent (id, token)
    return {
        'owner': owner_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details,
        'donald': donald_details
    }

def test_user_profile_valid_own(user_data):
    '''
    Testing users checking their own profiles
    '''
    profile_data = user_profile(user_data['owner']['token'], user_data['owner']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['owner']['u_id'],
            'email': 'owner@email.com',
            'name_first': 'owner_first',
            'name_last': 'owner_last',
            'handle_str': 'owner_firstowner_las',
        }
    }

    assert profile_data == exp_dict

    profile_data = user_profile(user_data['john']['token'], user_data['john']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['john']['u_id'],
            'email': 'johnsmith@gmail.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_else(user_data):
    '''
    Testing users checking other user's profiles
    '''

    profile_data = user_profile(user_data['john']['token'], user_data['jane']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['jane']['u_id'],
            'email': 'janesmith@hotmail.com',
            'name_first': 'Jane',
            'name_last': 'Smith',
            'handle_str': 'janesmith',
        },
    }

    assert profile_data == exp_dict

    profile_data = user_profile(user_data['jane']['token'], user_data['ingrid']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['ingrid']['u_id'],
            'email': 'ingrid.cline@gmail.com',
            'name_first': 'Ingrid',
            'name_last': 'Cline',
            'handle_str': 'ingridcline',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_valid_logout(user_data):
    '''
    Testing the retrieval of profile data from a user that is logged out
    by a user that is logged in
    '''

    auth_logout(user_data['john']['token'])

    profile_data = user_profile(user_data['jane']['token'], user_data['john']['u_id'])

    exp_dict = {
        'user': {
            'u_id': user_data['john']['u_id'],
            'email': 'johnsmith@gmail.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
        },
    }

    assert profile_data == exp_dict

def test_user_profile_invalid_uid(user_data):
    '''
    Testing user_profile with an invalid u_id parameter
    '''
    
    invalid_uid = -1

    with pytest.raises(InputError):
        user_profile(user_data['jane']['token'], invalid_uid)

def test_user_profile_invalid_token(user_data):
    '''
    Testing user_profile with an invalid token parameter
    '''

    invalid_token = user_data['john']['token']
    auth_logout(user_data['john']['token'])

    with pytest.raises(AccessError):
        user_profile(invalid_token, user_data['jane']['u_id'])

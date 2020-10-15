from auth import auth_register, auth_logout
from other import clear, users_all
from error import AccessError, InputError
import pytest

# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Cyrus Wilkie

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> user_data() return {users}
-> test_users_all_basic(user_data)
-> test_users_all_logout(user_data)
-> test_users_all_invalid_token(user_data)
'''

@pytest.fixture
def user_data():
    '''
    Sets up various user sample data for testing purposes
    '''

    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John', 'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', 'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', 'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', 'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df', 'Donald', 'Richards')

    # Returns user data that is implementation dependent (id, token)
    return {
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details,
        'donald': donald_details, 
    }

def test_users_all_basic(user_data):
    '''
    Basic valid test case of users_all
    '''

    all_users = users_all(user_data['john']['token'])

    exp_dict = {
        'users': [
            {
                'u_id': user_data['john']['u_id'],
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': user_data['jane']['u_id'],
                'email': 'janesmith@hotmail.com',
                'name_first': 'Jane',
                'name_last': 'Smith',
                'handle_str': 'janesmith',
            },
            {
                'u_id': user_data['noah']['u_id'],
                'email': 'noah_navarro@yahoo.com',
                'name_first': 'Noah',
                'name_last': 'Navarro',
                'handle_str': 'noahnavarro',
            },
            {
                'u_id': user_data['ingrid']['u_id'],
                'email': 'ingrid.cline@gmail.com',
                'name_first': 'Ingrid',
                'name_last': 'Cline',
                'handle_str': 'ingridcline',
            },
            {
                'u_id': user_data['donald']['u_id'],
                'email': 'donaldrichards@gmail.com',
                'name_first': 'Donald',
                'name_last': 'Richards',
                'handle_str': 'donaldrichards',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_logout(user_data):
    '''
    Tests that all user profiles are returned even if
    some users are logged out
    '''

    auth_logout(user_data['jane']['token'])
    auth_logout(user_data['donald']['token'])

    all_users = users_all(user_data['john']['token'])

    exp_dict = {
        'users': [
            {
                'u_id': user_data['john']['u_id'],
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': user_data['jane']['u_id'],
                'email': 'janesmith@hotmail.com',
                'name_first': 'Jane',
                'name_last': 'Smith',
                'handle_str': 'janesmith',
            },
            {
                'u_id': user_data['noah']['u_id'],
                'email': 'noah_navarro@yahoo.com',
                'name_first': 'Noah',
                'name_last': 'Navarro',
                'handle_str': 'noahnavarro',
            },
            {
                'u_id': user_data['ingrid']['u_id'],
                'email': 'ingrid.cline@gmail.com',
                'name_first': 'Ingrid',
                'name_last': 'Cline',
                'handle_str': 'ingridcline',
            },
            {
                'u_id': user_data['donald']['u_id'],
                'email': 'donaldrichards@gmail.com',
                'name_first': 'Donald',
                'name_last': 'Richards',
                'handle_str': 'donaldrichards',
            },
        ],
    }

    assert all_users == exp_dict

def test_users_all_invalid_token(user_data):
    '''
    Testing users_all with an invalid token parameter
    '''

    invalid_token = user_data['john']['token']
    auth_logout(user_data['john']['token'])

    with pytest.raises(AccessError):
        users_all(invalid_token)
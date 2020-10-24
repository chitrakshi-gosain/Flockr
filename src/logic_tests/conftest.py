import pytest
from auth import auth_register
from channels import channels_create
from other import clear

@pytest.fixture
def reset():
    '''
    Resets the internal data of the application to it's initial state
    '''
    
    clear()


@pytest.fixture
def initialise_user_data(reset):
    '''
    Sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    admin_details = auth_register('admin@email.com', 'admin_pass1!', 'admin_first', 'admin_last')

    owner_details = auth_register('owner@email.com', 'owner_pass1!', 'owner_first', 'owner_last')

    user0_details = auth_register('user0@email.com', 'user0_pass1!', 'user0_first', 'user0_last')

    user1_details = auth_register('user1@email.com', 'user1_pass1!', 'user1_first', 'user1_last')

    user2_details = auth_register('user2@email.com', 'user2_pass1!', 'user2_first', 'user2_last')

    user3_details = auth_register('user3@email.com', 'user3_pass1!', 'user3_first', 'user3_last')

    return {
        'admin': admin_details,
        'owner': owner_details,
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details
    }

@pytest.fixture
def initialise_channel_data(url, initialise_user_data):
    '''
    creates 3 channels with descriptive data for testing
    '''

    admin_token = initialise_user_data['admin']['token']
    admin_public_details = channels_create(admin_token, 'admin_public', True)
    admin_private_details = channels_create(admin_token, 'admin_private1', False)

    owner_token = initialise_user_data['owner']['token']
    owner_public_details = channels_create(owner_token, 'owner_public', True)
    owner_private_details = channels_create(owner_token, 'owner_private1', False)

    user_token = initialise_user_data['user1']['token']
    user_private_details = channels_create(user_token, 'private', False)

    return {
        'admin_publ': admin_public_details,
        'admin_priv': admin_private_details,
        'owner_publ': owner_public_details,
        'owner_priv': owner_private_details,
        'user1_priv': user_private_details
    }

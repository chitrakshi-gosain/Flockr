'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 1
'''

import pytest
from auth import auth_logout
from channels import channels_create, channels_list
from error import AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> channels_list(token) return {channels}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_channels_list_valid_single(initialise_user_data):
    '''
    Listing a single created channel
    '''
    users = initialise_user_data

    # Creating a basic public channel
    channel_id = channels_create(users['owner']['token'], 'A Basic Channel', True)

    # Checking channels_list return is correct
    channel_list = channels_list(users['owner']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'A Basic Channel'

    # Type checking
    assert isinstance(channel_list['channels'][0]['channel_id'], int)
    assert isinstance(channel_list['channels'][0]['name'], str)


def test_channels_list_valid_same(initialise_user_data):
    '''
    Listing multiple created channels from the same user
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user1']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['user1']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['user1']['token'], 'Chatter', True))
    channel_id.append(channels_create(users['user1']['token'], '3rd Channel', True))

    # Checking channels_list return is correct
    channel_list = channels_list(users['user1']['token'])

    # Id checks
    assert channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id[1]['channel_id']
    assert channel_list['channels'][2]['channel_id'] == channel_id[2]['channel_id']
    assert channel_list['channels'][3]['channel_id'] == channel_id[3]['channel_id']
    assert channel_list['channels'][4]['channel_id'] == channel_id[4]['channel_id']

    # Name checks
    assert channel_list['channels'][0]['name'] == 'First Channel'
    assert channel_list['channels'][1]['name'] == 'Channel 2'
    assert channel_list['channels'][2]['name'] == 'Discussion'
    assert channel_list['channels'][3]['name'] == 'Chatter'
    assert channel_list['channels'][4]['name'] == '3rd Channel'


def test_channels_list_valid_different(initialise_user_data):
    '''
    Listing multiple created channels from different users
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['user3']['token'], 'Discussion', True))

    # Checking channels_list return is correct
    user1_channel_list = channels_list(users['user1']['token'])
    user2_channel_list = channels_list(users['user2']['token'])
    user3_channel_list = channels_list(users['user3']['token'])

    # Id checks
    assert user1_channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert user2_channel_list['channels'][0]['channel_id'] == channel_id[1]['channel_id']
    assert user3_channel_list['channels'][0]['channel_id'] == channel_id[2]['channel_id']

    # Name checks
    assert user1_channel_list['channels'][0]['name'] == 'First Channel'
    assert user2_channel_list['channels'][0]['name'] == 'Channel 2'
    assert user3_channel_list['channels'][0]['name'] == 'Discussion'


def test_channels_list_valid_private(initialise_user_data):
    '''
    Listing multiple created private channels from different users
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user1']['token'], 'Channel 2', False))
    channel_id.append(channels_create(users['user2']['token'], 'Discussion', False))
    channel_id.append(channels_create(users['user2']['token'], 'Chatter', False))
    channel_id.append(channels_create(users['user2']['token'], '3rd Channel', False))

    # Checking channels_list return is correct
    user1_channel_list = channels_list(users['user1']['token'])
    user2_channel_list = channels_list(users['user2']['token'])

    # Id checks
    assert user1_channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert user1_channel_list['channels'][1]['channel_id'] == channel_id[1]['channel_id']
    assert user2_channel_list['channels'][0]['channel_id'] == channel_id[2]['channel_id']
    assert user2_channel_list['channels'][1]['channel_id'] == channel_id[3]['channel_id']
    assert user2_channel_list['channels'][2]['channel_id'] == channel_id[4]['channel_id']

    # Name checks
    assert user1_channel_list['channels'][0]['name'] == 'First Channel'
    assert user1_channel_list['channels'][1]['name'] == 'Channel 2'
    assert user2_channel_list['channels'][0]['name'] == 'Discussion'
    assert user2_channel_list['channels'][1]['name'] == 'Chatter'
    assert user2_channel_list['channels'][2]['name'] == '3rd Channel'


def test_channels_list_valid_mix(initialise_user_data):
    '''
    Listing a mix of multiple public and private channels from different users with some sharing names
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['user3']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user3']['token'], 'Channel 2', False))

    # Checking channels_list return is correct
    user1_channel_list = channels_list(users['user1']['token'])
    user2_channel_list = channels_list(users['user2']['token'])
    user3_channel_list = channels_list(users['user3']['token'])

    # Id checks
    assert user1_channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert user2_channel_list['channels'][0]['channel_id'] == channel_id[1]['channel_id']
    assert user3_channel_list['channels'][0]['channel_id'] == channel_id[2]['channel_id']
    assert user1_channel_list['channels'][1]['channel_id'] == channel_id[3]['channel_id']
    assert user3_channel_list['channels'][1]['channel_id'] == channel_id[4]['channel_id']

    # Name checks
    assert user1_channel_list['channels'][0]['name'] == 'First Channel'
    assert user2_channel_list['channels'][0]['name'] == 'Channel 2'
    assert user3_channel_list['channels'][0]['name'] == 'Discussion'
    assert user1_channel_list['channels'][1]['name'] == 'First Channel'
    assert user3_channel_list['channels'][1]['name'] == 'Channel 2'


def test_channels_list_valid_empty(initialise_user_data):
    '''
    Listing channels when none have been created
    '''
    users = initialise_user_data

    # Checking channels_list return is correct
    assert channels_list(users['user1']['token']) == {'channels': []}

def test_channels_list_invalid_token(initialise_user_data):
    '''
    Attempting to call channels_list without a valid token
    '''
    users = initialise_user_data

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(AccessError):
        channels_list(invalid_token)

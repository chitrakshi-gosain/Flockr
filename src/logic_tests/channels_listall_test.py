'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 1
'''

import pytest
from auth import auth_logout
from channels import channels_create, channels_listall
from error import AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> channels_listall(token) return {channels}
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


def test_channels_listall_valid_single(initialise_user_data):
    '''
    Listing a single created channel
    '''
    users = initialise_user_data

    # Creating a basic public channel
    channel_id = channels_create(users['owner']['token'], 'A Basic Channel', True)

    # Checking channels_list return is correct
    channel_list = channels_listall(users['owner']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'A Basic Channel'

    # Type checking
    assert isinstance(channel_list['channels'][0]['channel_id'], int)
    assert isinstance(channel_list['channels'][0]['name'], str)

def test_channels_listall_valid_same(initialise_user_data):
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
    channel_list = channels_listall(users['user1']['token'])

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

def test_channels_listall_valid_different(initialise_user_data):
    '''
    Listing multiple created channels from different users
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['user3']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['user0']['token'], 'Chatter', True))
    channel_id.append(channels_create(users['user0']['token'], '3rd Channel', True))

    # Checking channels_list return is correct
    channel_list = channels_listall(users['user1']['token'])

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

def test_channels_listall_valid_private(initialise_user_data):
    '''
    Listing multiple created private channels from different users
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', False))
    channel_id.append(channels_create(users['user3']['token'], 'Discussion', False))
    channel_id.append(channels_create(users['user3']['token'], 'Chatter', False))
    channel_id.append(channels_create(users['user3']['token'], '3rd Channel', False))

    # Checking channels_list return is correct
    channel_list = channels_listall(users['user1']['token'])

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

def test_channels_listall_valid_mix(initialise_user_data):
    '''
    Listing a mix of multiple public and private channels from different users with some sharing names
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['user3']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['user2']['token'], 'Chatter', True))
    channel_id.append(channels_create(users['user3']['token'], '3rd Channel', True))
    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user3']['token'], 'Channel 2', False))
    channel_id.append(channels_create(users['user0']['token'], 'Private', False))

    # Checking channels_list return is correct
    channel_list = channels_listall(users['user1']['token'])

    # Id checks
    assert channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id[1]['channel_id']
    assert channel_list['channels'][2]['channel_id'] == channel_id[2]['channel_id']
    assert channel_list['channels'][3]['channel_id'] == channel_id[3]['channel_id']
    assert channel_list['channels'][4]['channel_id'] == channel_id[4]['channel_id']
    assert channel_list['channels'][5]['channel_id'] == channel_id[5]['channel_id']
    assert channel_list['channels'][6]['channel_id'] == channel_id[6]['channel_id']
    assert channel_list['channels'][7]['channel_id'] == channel_id[7]['channel_id']

    # Name checks
    assert channel_list['channels'][0]['name'] == 'First Channel'
    assert channel_list['channels'][1]['name'] == 'Channel 2'
    assert channel_list['channels'][2]['name'] == 'Discussion'
    assert channel_list['channels'][3]['name'] == 'Chatter'
    assert channel_list['channels'][4]['name'] == '3rd Channel'
    assert channel_list['channels'][5]['name'] == 'First Channel'
    assert channel_list['channels'][6]['name'] == 'Channel 2'
    assert channel_list['channels'][7]['name'] == 'Private'

def test_channels_listall_valid_empty(initialise_user_data):
    '''
    Listing channels when none have been created
    '''
    users = initialise_user_data

    # Checking channels_list return is correct
    assert channels_listall(users['user1']['token']) == {'channels': []}

def test_channels_listall_invalid_token(initialise_user_data):
    '''
    Attempting to call channels_listall without a valid token
    '''
    users = initialise_user_data

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(AccessError):
        channels_listall(invalid_token)

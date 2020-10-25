'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 1
'''

import pytest
from auth import  auth_logout
from channel import channel_details, channel_join
from channels import channels_create, channels_listall
from error import AccessError, InputError

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> channel_details(token, channel_id) return {channel}
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
Error type: InputError
    -> channel name is more than 20 characters long
'''

def test_channels_create_valid_basic(initialise_user_data):
    '''
    Creating channel with valid data
    '''
    users = initialise_user_data

    # Creating a basic public channel
    channel_id = channels_create(users['owner']['token'], 'A Basic Channel', True)

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    basic_channel_details = channel_details(users['owner']['token'], channel_id['channel_id'])

    assert basic_channel_details['name'] == 'A Basic Channel'
    assert basic_channel_details['owner_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['owner_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['owner_members'][0]['name_last'] == 'owner_last'
    assert basic_channel_details['all_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['all_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['all_members'][0]['name_last'] == 'owner_last'

def test_channels_create_valid_empty(initialise_user_data):
    '''
    Creating channel with empty string name
    '''
    users = initialise_user_data

    # Creating public channel with empty string as name
    channel_id = channels_create(users['user1']['token'], '', True)

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    empty_channel_details = channel_details(users['user1']['token'], channel_id['channel_id'])

    assert empty_channel_details['name'] == ''
    assert empty_channel_details['owner_members'][0]['u_id'] == users['user1']['u_id']
    assert empty_channel_details['owner_members'][0]['name_first'] == 'user1_first'
    assert empty_channel_details['owner_members'][0]['name_last'] == 'user1_last'
    assert empty_channel_details['all_members'][0]['u_id'] == users['user1']['u_id']
    assert empty_channel_details['all_members'][0]['name_first'] == 'user1_first'
    assert empty_channel_details['all_members'][0]['name_last'] == 'user1_last'

def test_channels_create_valid_private(initialise_user_data):
    '''
    Creating private channel
    '''
    users = initialise_user_data

    # Creating private channel
    channel_id = channels_create(users['user1']['token'], 'Private Disc', False)

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    private_channel_details = channel_details(users['user1']['token'], channel_id['channel_id'])

    assert private_channel_details['name'] == 'Private Disc'
    assert private_channel_details['owner_members'][0]['u_id'] == users['user1']['u_id']
    assert private_channel_details['owner_members'][0]['name_first'] == 'user1_first'
    assert private_channel_details['owner_members'][0]['name_last'] == 'user1_last'
    assert private_channel_details['all_members'][0]['u_id'] == users['user1']['u_id']
    assert private_channel_details['all_members'][0]['name_first'] == 'user1_first'
    assert private_channel_details['all_members'][0]['name_last'] == 'user1_last'

    # Ensure that channel is private by attempting join from non-member
    with pytest.raises(AccessError):
        channel_join(users['user1']['token'], channel_id['channel_id'])

def test_channels_create_invalid_namesize(initialise_user_data):
    '''
    Creating channel with too large of a name
    '''
    users = initialise_user_data

    # Creating public channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create(users['user1']['token'], 'supercalifragilisticexpialidocious', True)

    # Creating private channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create(users['user2']['token'], 'supercalifragilisticexpialidocious', False)

def test_channels_create_valid_samename(initialise_user_data):
    '''
    Creating two channels with the same name
    '''
    users = initialise_user_data

    # Creating public channels with the same name
    channel_id1 = channels_create(users['user1']['token'], 'Hello World!', True)
    channel_id2 = channels_create(users['user2']['token'], 'Hello World!', True)

    # Checking both channels exist and have the same name
    channel_list = channels_listall(users['user3']['token'])

    assert channel_list['channels'][0]['name'] == 'Hello World!'
    assert channel_list['channels'][1]['name'] == 'Hello World!'
    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']


def test_channels_create_invalid_token(initialise_user_data):
    '''
    Attempting to call channels_listall without a valid token
    '''
    users = initialise_user_data

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(AccessError):
        channels_create(invalid_token, 'Name', True)

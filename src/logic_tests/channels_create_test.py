from auth import auth_register, auth_logout
from channel import channel_details, channel_join
from channels import channels_create, channels_listall
from other import clear
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
-> intialise_user_data() return {users}
-> test_channels_create_valid_basic()
-> test_channels_create_valid_empty()
-> test_channels_create_valid_private()
-> test_channels_create_invalid_namesize()
-> test_channels_create_valid_samename()
-> test_channels_create_invalid_token()
'''

'''
----channels_create Documentation----
Parameters:
(token, name, is_public)

Return Type:
{channel_id}

Exceptions:
InputError when any of:
- Name is more than 20 characters long

Description:
Creates a new channel with that name 
that is either a public or private channel
'''

def initialise_user_data():
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


def test_channels_create_valid_basic():
    '''
    Creating channel with valid data
    '''

    users = initialise_user_data()

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

    clear()


def test_channels_create_valid_empty():
    '''
    Creating channel with empty string name
    '''

    users = initialise_user_data()

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

    clear()


def test_channels_create_valid_private():
    '''
    Creating private channel
    '''

    users = initialise_user_data()

    # Creating private channel
    channel_id = channels_create(users['john']['token'], 'Private Disc', False)

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    private_channel_details = channel_details(users['john']['token'], channel_id['channel_id'])

    assert private_channel_details['name'] == 'Private Disc'
    assert private_channel_details['owner_members'][0]['u_id'] == users['john']['u_id']
    assert private_channel_details['owner_members'][0]['name_first'] == 'John'
    assert private_channel_details['owner_members'][0]['name_last'] == 'Smith'
    assert private_channel_details['all_members'][0]['u_id'] == users['john']['u_id']
    assert private_channel_details['all_members'][0]['name_first'] == 'John'
    assert private_channel_details['all_members'][0]['name_last'] == 'Smith'

    # Ensure that channel is private by attempting join from non-member
    with pytest.raises(AccessError):
        channel_join(users['user1']['token'], channel_id['channel_id'])

    clear()


def test_channels_create_invalid_namesize():
    '''
    Creating channel with too large of a name
    '''

    users = initialise_user_data()

    # Creating public channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create(users['user1']['token'], 'supercalifragilisticexpialidocious', True)

    # Creating private channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create(users['user2']['token'], 'supercalifragilisticexpialidocious', False)

    clear()


def test_channels_create_valid_samename():
    '''
    Creating two channels with the same name
    '''

    users = initialise_user_data()

    # Creating public channels with the same name
    channel_id1 = channels_create(users['user1']['token'], 'Hello World!', True)
    channel_id2 = channels_create(users['user2']['token'], 'Hello World!', True)

    # Checking both channels exist and have the same name
    channel_list = channels_listall(users['user3']['token'])

    assert channel_list['channels'][0]['name'] == 'Hello World!'
    assert channel_list['channels'][1]['name'] == 'Hello World!'
    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']


def test_channels_create_invalid_token():
    '''
    Attempting to call channels_listall without a valid token
    '''

    users = initialise_user_data()

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(AccessError):
        channels_create(invalid_token, 'Name', True)

    clear()
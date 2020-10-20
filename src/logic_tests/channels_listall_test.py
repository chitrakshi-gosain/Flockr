from auth import auth_register, auth_logout
from channel import channel_details
from channels import channels_create, channels_listall, channels_list
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
-> test_channels_listall_valid_single()
-> test_channels_listall_valid_same()
-> test_channels_listall_valid_different()
-> test_channels_listall_valid_private()
-> test_channels_listall_valid_mix()
-> test_channels_listall_valid_empty()
-> test_channels_listall_invalid_token()
'''

'''
----channels_listall Documentation----
Parameters:
(token)

Return Type:
{channels}

Exceptions:
N/A

Description:
Provide a list of all channels (and 
their associated details)
'''

@pytest.fixture
def users():
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


def test_channels_listall_valid_single(users):
    '''
    Listing a single created channel
    '''

    # Creating a basic public channel
    channel_id = channels_create(users['owner']['token'], 'A Basic Channel', True)

    # Checking channels_list return is correct
    channel_list = channels_listall(users['owner']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'A Basic Channel'

    # Type checking
    assert isinstance(channel_list['channels'][0]['channel_id'], int)
    assert isinstance(channel_list['channels'][0]['name'], str)

    clear()


def test_channels_listall_valid_same(users):
    '''
    Listing multiple created channels from the same user
    '''

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

    clear()


def test_channels_listall_valid_different(users):
    '''
    Listing multiple created channels from different users
    '''

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['donald']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['john']['token'], 'Chatter', True))
    channel_id.append(channels_create(users['ingrid']['token'], '3rd Channel', True))

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

    clear()


def test_channels_listall_valid_private(users):
    '''
    Listing multiple created private channels from different users
    '''

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', False))
    channel_id.append(channels_create(users['donald']['token'], 'Discussion', False))
    channel_id.append(channels_create(users['john']['token'], 'Chatter', False))
    channel_id.append(channels_create(users['ingrid']['token'], '3rd Channel', False))

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

    clear()


def test_channels_listall_valid_mix(users):
    '''
    Listing a mix of multiple public and private channels from different users with some sharing names
    '''

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(channels_create(users['user1']['token'], 'First Channel', True))
    channel_id.append(channels_create(users['user2']['token'], 'Channel 2', True))
    channel_id.append(channels_create(users['donald']['token'], 'Discussion', True))
    channel_id.append(channels_create(users['john']['token'], 'Chatter', True))
    channel_id.append(channels_create(users['ingrid']['token'], '3rd Channel', True))
    channel_id.append(channels_create(users['user1']['token'], 'First Channel', False))
    channel_id.append(channels_create(users['user3']['token'], 'Channel 2', False))
    channel_id.append(channels_create(users['jane']['token'], 'Private', False))

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

    clear()


def test_channels_listall_valid_empty(users):
    '''
    Listing channels when none have been created
    '''

    # Checking channels_list return is correct
    assert channels_listall(users['user1']['token']) == {'channels': []}

    clear()


def test_channels_listall_invalid_token(users):
    '''
    Attempting to call channels_listall without a valid token
    '''

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(AccessError):
        channels_listall(invalid_token)

    clear()
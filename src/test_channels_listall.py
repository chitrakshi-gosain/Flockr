from auth import auth_register, auth_logout
from channel import channel_details
from channels import channels_create, channels_listall, channels_list
from other import clear
import pytest

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

# Sets up various user sample data for testing purposes
def initialise_user_data():
    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Descriptive test data
    owner_details = auth_register('owner@email.com', 'owner_pass', 'owner_first', 'owner_last')
    user1_details = auth_register('user1@email.com', 'user1_pass', 'user1_first', 'user1_last')
    user2_details = auth_register('user2@email.com', 'user2_pass', 'user2_first', 'user2_last')
    user3_details = auth_register('user3@email.com', 'user3_pass', 'user3_first', 'user3_last')
    user4_details = auth_register('user4@email.com', 'user4_pass', 'user4_first', 'user4_last')
    user5_details = auth_register('user5@email.com', 'user5_pass', 'user5_first', 'user5_last')

    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qwertyuiop', 'John', 'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'mydateofbirth', 'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RPassWord', 'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o75630', 'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjdfg;h;;df', 'Donald', 'Richards')

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

# Listing a single created channel
def test_channels_listall_valid_single():
    users = initialise_user_data()

    # Creating a basic public channel
    channel_id = channels_create(users['owner']['token'], 'A Basic Channel', True)

    # Checking channels_list return is correct
    channel_list = channels_listall(users['owner']['token'])

    assert channel_list[0]['channel_id'] == channel_id
    assert channel_list[0]['name'] == 'A Basic Channel'

    clear()

# Listing multiple created channels from the same user
def test_channels_listall_valid_same():
    users = initialise_user_data()

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
    assert channel_list[0]['channel_id'] == channel_id[0]
    assert channel_list[1]['channel_id'] == channel_id[1]
    assert channel_list[2]['channel_id'] == channel_id[2]
    assert channel_list[3]['channel_id'] == channel_id[3]
    assert channel_list[4]['channel_id'] == channel_id[4]

    # Name checks
    assert channel_list[0]['name'] == 'First Channel'
    assert channel_list[1]['name'] == 'Channel 2'
    assert channel_list[2]['name'] == 'Discussion'
    assert channel_list[3]['name'] == 'Chatter'
    assert channel_list[4]['name'] == '3rd Channel'

    clear()

# Listing multiple created channels from different users
def test_channels_listall_valid_same():
    users = initialise_user_data()

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
    assert channel_list[0]['channel_id'] == channel_id[0]
    assert channel_list[1]['channel_id'] == channel_id[1]
    assert channel_list[2]['channel_id'] == channel_id[2]
    assert channel_list[3]['channel_id'] == channel_id[3]
    assert channel_list[4]['channel_id'] == channel_id[4]

    # Name checks
    assert channel_list[0]['name'] == 'First Channel'
    assert channel_list[1]['name'] == 'Channel 2'
    assert channel_list[2]['name'] == 'Discussion'
    assert channel_list[3]['name'] == 'Chatter'
    assert channel_list[4]['name'] == '3rd Channel'

    clear()

# Listing multiple created private channels from different users
def test_channels_listall_valid_private():
    users = initialise_user_data()

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
    assert channel_list[0]['channel_id'] == channel_id[0]
    assert channel_list[1]['channel_id'] == channel_id[1]
    assert channel_list[2]['channel_id'] == channel_id[2]
    assert channel_list[3]['channel_id'] == channel_id[3]
    assert channel_list[4]['channel_id'] == channel_id[4]

    # Name checks
    assert channel_list[0]['name'] == 'First Channel'
    assert channel_list[1]['name'] == 'Channel 2'
    assert channel_list[2]['name'] == 'Discussion'
    assert channel_list[3]['name'] == 'Chatter'
    assert channel_list[4]['name'] == '3rd Channel'

    clear()

# Listing a mix of multiple public and private channels from different users with some sharing names
def test_channels_listall_valid_mix():
    users = initialise_user_data()

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
    assert channel_list[0]['channel_id'] == channel_id[0]
    assert channel_list[1]['channel_id'] == channel_id[1]
    assert channel_list[2]['channel_id'] == channel_id[2]
    assert channel_list[3]['channel_id'] == channel_id[3]
    assert channel_list[4]['channel_id'] == channel_id[4]
    assert channel_list[5]['channel_id'] == channel_id[5]
    assert channel_list[6]['channel_id'] == channel_id[6]
    assert channel_list[7]['channel_id'] == channel_id[7]

    # Name checks
    assert channel_list[0]['name'] == 'First Channel'
    assert channel_list[1]['name'] == 'Channel 2'
    assert channel_list[2]['name'] == 'Discussion'
    assert channel_list[3]['name'] == 'Chatter'
    assert channel_list[4]['name'] == '3rd Channel'
    assert channel_list[5]['name'] == 'First Channel'
    assert channel_list[6]['name'] == 'Channel 2'
    assert channel_list[7]['name'] == 'Private'

    clear()

# Listing channels when none have been created
def test_channels_listall_valid_empty():
    users = initialise_user_data()

    # Checking channels_list return is correct
    assert channels_listall(users['user1']['token']) == []

    clear()

# Attempting to call channels_listall without a valid token
def test_channels_listall_invalid_token():
    users = initialise_user_data()

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    auth_logout(invalid_token)

    # Checking that AccessError is thrown
    with pytest.raises(Exception):
        channels_listall(invalid_token)

    clear()
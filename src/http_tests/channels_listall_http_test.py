'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route(.....) return json.dumps({...})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_users
'''

'''
EXCEPTIONS
Error type: AccessError
    -> Invalid token
'''

@pytest.fixture
def intialise_users(url):
    '''
    Sets up various user sample data for testing purposes
    '''

    # Register users:
    # Descriptive test data
    owner_details = requests.post(f'{url}/auth/register', json={
        'email': 'owner@email.com',
        'password': 'Owner_pass1!',
        'name_first': 'owner_first',
        'name_last': 'owner_last',
    }).json()
    user1_details = requests.post(f'{url}/auth/register', json={
        'email': 'user1@email.com',
        'password': 'User1_pass!',
        'name_first': 'user1_first',
        'name_last': 'user1_last',
    }).json()
    user2_details = requests.post(f'{url}/auth/register', json={
        'email': 'user2@email.com',
        'password': 'User2_pass!',
        'name_first': 'user2_first',
        'name_last': 'user2_last',
    }).json()
    user3_details = requests.post(f'{url}/auth/register', json={
        'email': 'user3@email.com',
        'password': 'User3_pass!',
        'name_first': 'user3_first',
        'name_last': 'user3_last',
    }).json()
    user4_details = requests.post(f'{url}/auth/register', json={
        'email': 'user4@email.com',
        'password': 'User4_pass!',
        'name_first': 'user4_first',
        'name_last': 'user4_last',
    }).json()
    user5_details = requests.post(f'{url}/auth/register', json={
        'email': 'user5@email.com',
        'password': 'User5_pass!',
        'name_first': 'user5_first',
        'name_last': 'user5_last',
    }).json()

    # Realistic test data
    john_details = requests.post(f'{url}/auth/register', json={
        'email': 'johnsmith@gmail.com',
        'password': 'qweRt1uiop!',
        'name_first': 'John',
        'name_last': 'Smith',
    }).json()
    jane_details = requests.post(f'{url}/auth/register', json={
        'email': 'janesmith@hotmail.com',
        'password': 'm3yDate0fb!rth',
        'name_first': 'Jane',
        'name_last': 'Smith',
    }).json()
    noah_details = requests.post(f'{url}/auth/register', json={
        'email': 'noah_navarro@yahoo.com',
        'password': 'aP00RP&ssWord1',
        'name_first': 'Noah',
        'name_last': 'Navarro',
    }).json()
    ingrid_details = requests.post(f'{url}/auth/register', json={
        'email': 'ingrid.cline@gmail.com',
        'password': '572o7563O*',
        'name_first': 'Ingrid',
        'name_last': 'Cline',
    }).json()
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df', 'Donald', 'Richards')
    donald_details = requests.post(f'{url}/auth/register', json={
        'email': 'donaldrichards@gmail.com',
        'password': 'kjDf2g@h@@df',
        'name_first': 'Donald',
        'name_last': 'Richards',
    }).json()

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

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_channels_listall_valid_single(initialise_users):
    '''
    Listing a single created channel
    '''
    users = initialise_users

    # Creating a basic public channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['owner']['token'],
        'name': 'A Basic Channel',
        'is_public': True,
    }).json()

    # Checking channels_list return is correct
    channel_list = requests.get(f'{url}/channels/listall', json={
        'token': users['owner']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'A Basic Channel'

    # Type checking
    assert isinstance(channel_list['channels'][0]['channel_id'], int)
    assert isinstance(channel_list['channels'][0]['name'], str)

def test_channels_listall_valid_same(initialise_users):
    '''
    Listing multiple created channels from the same user
    '''
    users = initialise_users

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'First Channel',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'Channel 2',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'Discussion',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'Chatter',
        'is_public': True,
    }).json())
    channel_id.append(channels_create(users['user1']['token'], '3rd Channel', True))
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': '3rd Channel',
        'is_public': True,
    }).json())

    # Checking channels_list return is correct
    channel_list = requests.get(f'{url}/channels/listall', json={
        'token': users['user1']['token'],
    }).json()

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

def test_channels_listall_valid_different(initialise_users):
    '''
    Listing multiple created channels from different users
    '''
    users = initialise_users

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'First Channel',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': 'Channel 2',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['donald']['token'],
        'name': 'Discussion',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['john']['token'],
        'name': 'Chatter',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['ingrid']['token'],
        'name': '3rd Channel',
        'is_public': True,
    }).json())

    # Checking channels_list return is correct
    channel_list = requests.get(f'{url}/channels/listall', json={
        'token': users['user1']['token'],
    }).json()

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


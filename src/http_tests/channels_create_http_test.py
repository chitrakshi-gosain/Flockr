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
-> ...
'''

'''
EXCEPTIONS
Error type: InputError
    -> ..
Error type: AccessError
    -> ..
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

def test_channels_create_valid_basic(intialise_users):
    '''
    Creating channel with valid data
    '''
    users = intialise_users

    # Creating a basic public channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['owner']['token']
        'name': 'A Basic Channel'
        'is_public': True
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    basic_channel_details = requests.get(f'{url}/channel/details', json={
        'token': users['owner']['token']
        'channel_id': channel_id['channel_id']
    }).json()

    assert basic_channel_details['name'] == 'A Basic Channel'
    assert basic_channel_details['owner_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['owner_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['owner_members'][0]['name_last'] == 'owner_last'
    assert basic_channel_details['all_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['all_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['all_members'][0]['name_last'] == 'owner_last'

def test_channels_create_valid_empty(users):
    '''
    Creating channel with empty string name
    '''

    # Creating public channel with empty string as name
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token']
        'name': ''
        'is_public': True
    }).json()

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
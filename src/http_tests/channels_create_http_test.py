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
-> APP.route("/channels/create", methods=['POST']) return json.dumps({channel_id})
-> APP.route("/channel/details", methods=['GET']) return json.dumps({name, owner_members, all_members})
-> APP.route("/channels/listall", methods=['GET']) return json.dumps({channels})
-> APP.route("/auth/logout", methods=['POST']) return json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> intialise_users
'''

'''
EXCEPTIONS
Error type: InputError
    -> Name is more then 20 characters long
Error type: AccessError
    -> Invalid token
'''

@pytest.fixture
def initialise_users(url):
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

def test_channels_create_valid_basic(url, initialise_users):
    '''
    Creating channel with valid data
    '''
    users = intialise_users

    # Creating a basic public channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['owner']['token'],
        'name': 'A Basic Channel',
        'is_public': True,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    basic_channel_details = requests.get(f'{url}/channel/details', json={
        'token': users['owner']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert basic_channel_details['name'] == 'A Basic Channel'
    assert basic_channel_details['owner_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['owner_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['owner_members'][0]['name_last'] == 'owner_last'
    assert basic_channel_details['all_members'][0]['u_id'] == users['owner']['u_id']
    assert basic_channel_details['all_members'][0]['name_first'] == 'owner_first'
    assert basic_channel_details['all_members'][0]['name_last'] == 'owner_last'

def test_channels_create_valid_empty(url, initialise_users):
    '''
    Creating channel with empty string name
    '''
    users = initialise_users

    # Creating public channel with empty string as name
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': '',
        'is_public': True,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    empty_channel_details = requests.get(f'{url}/channel/details', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert empty_channel_details['name'] == ''
    assert empty_channel_details['owner_members'][0]['u_id'] == users['user1']['u_id']
    assert empty_channel_details['owner_members'][0]['name_first'] == 'user1_first'
    assert empty_channel_details['owner_members'][0]['name_last'] == 'user1_last'
    assert empty_channel_details['all_members'][0]['u_id'] == users['user1']['u_id']
    assert empty_channel_details['all_members'][0]['name_first'] == 'user1_first'
    assert empty_channel_details['all_members'][0]['name_last'] == 'user1_last'

def test_channels_create_valid_private(url, initialise_users):
    '''
    Creating private channel
    '''
    users = initialise_users

    # Creating private channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['john']['token'],
        'name': 'Private Disc',
        'is_public': False,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    private_channel_details = requests.get(f'{url}/channel/details', json={
        'token': users['john']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert private_channel_details['name'] == 'Private Disc'
    assert private_channel_details['owner_members'][0]['u_id'] == users['john']['u_id']
    assert private_channel_details['owner_members'][0]['name_first'] == 'John'
    assert private_channel_details['owner_members'][0]['name_last'] == 'Smith'
    assert private_channel_details['all_members'][0]['u_id'] == users['john']['u_id']
    assert private_channel_details['all_members'][0]['name_first'] == 'John'
    assert private_channel_details['all_members'][0]['name_last'] == 'Smith'

    # Ensure that channel is private by attempting join from non-member
    assert requests.post(f'{url}/channel/join', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).status_code == 400

def test_channels_create_invalid_namesize(url, initialise_users):
    '''
    Creating channel with too large of a name
    '''
    users = initialise_users

    # Creating public channel with namesize > 20 characters
    requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'supercalifragilisticexpialidocious',
        'is_public': True,
    }).status_code == 400

    # Creating private channel with namesize > 20 characters
    requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': 'supercalifragilisticexpialidocious',
        'is_public': False,
    }).status_code == 400

def test_channels_create_valid_samename(url, initialise_users):
    '''
    Creating two channels with the same name
    '''
    users = initialise_users

    # Creating public channels with the same name
    channel_id1 = requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'Hello World!',
        'is_public': True,
    }).json()
    channel_id2 = requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': 'Hello World!',
        'is_public': True,
    }).json()

    # Checking both channels exist and have the same name
    channel_list = requests.get(f'{url}/channels/listall', json={
        'token': users['user3']['token'],
    }).json()

    assert channel_list['channels'][0]['name'] == 'Hello World!'
    assert channel_list['channels'][1]['name'] == 'Hello World!'
    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']

def test_channels_create_invalid_token(url, initialise_users):
    '''
    Attempting to call channels_listall without a valid token
    '''
    users = initialise_users

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['owner']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    # Checking that AccessError is thrown
    assert requests.post(f'{url}/channels/create', json={
        'token': invalid_token,
        'name': 'Name',
        'is_public': True,
    }).status_code == 400

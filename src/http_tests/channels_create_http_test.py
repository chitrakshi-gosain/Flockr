'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
   json.dumps({channel_id})
-> APP.route("/channel/details", methods=['GET']) return
   json.dumps({name, owner_members, all_members})
-> APP.route("/channels/listall", methods=['GET']) return
   json.dumps({channels})
-> APP.route("/auth/logout", methods=['POST']) return
   json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> Name is more then 20 characters long
Error type: AccessError
    -> Invalid token
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_channels_create_valid_basic(url, initialise_user_data):
    '''
    Creating channel with valid data
    '''
    users = initialise_user_data

    # Creating a basic public channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user0']['token'],
        'name': 'A Basic Channel',
        'is_public': True,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    basic_channel_details = requests.get(f'{url}/channel/details', params={
        'token': users['user0']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert basic_channel_details['name'] == 'A Basic Channel'
    assert basic_channel_details['owner_members'][0]['u_id'] == users['user0']['u_id']
    assert basic_channel_details['owner_members'][0]['name_first'] == 'user0_first'
    assert basic_channel_details['owner_members'][0]['name_last'] == 'user0_last'
    assert basic_channel_details['all_members'][0]['u_id'] == users['user0']['u_id']
    assert basic_channel_details['all_members'][0]['name_first'] == 'user0_first'
    assert basic_channel_details['all_members'][0]['name_last'] == 'user0_last'

def test_channels_create_valid_empty(url, initialise_user_data):
    '''
    Creating channel with empty string name
    '''
    users = initialise_user_data

    # Creating public channel with empty string as name
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': '',
        'is_public': True,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    empty_channel_details = requests.get(f'{url}/channel/details', params={
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

def test_channels_create_valid_private(url, initialise_user_data):
    '''
    Creating private channel
    '''
    users = initialise_user_data

    # Creating private channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user0']['token'],
        'name': 'Private Disc',
        'is_public': False,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    private_channel_details = requests.get(f'{url}/channel/details', params={
        'token': users['user0']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert private_channel_details['name'] == 'Private Disc'
    assert private_channel_details['owner_members'][0]['u_id'] == users['user0']['u_id']
    assert private_channel_details['owner_members'][0]['name_first'] == 'user0_first'
    assert private_channel_details['owner_members'][0]['name_last'] == 'user0_last'
    assert private_channel_details['all_members'][0]['u_id'] == users['user0']['u_id']
    assert private_channel_details['all_members'][0]['name_first'] == 'user0_first'
    assert private_channel_details['all_members'][0]['name_last'] == 'user0_last'

    # Ensure that channel is private by attempting join from non-member
    assert requests.post(f'{url}/channel/join', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).status_code == 400

def test_channels_create_invalid_namesize(url, initialise_user_data):
    '''
    Creating channel with too large of a name
    '''
    users = initialise_user_data

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

def test_channels_create_valid_samename(url, initialise_user_data):
    '''
    Creating two channels with the same name
    '''
    users = initialise_user_data

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
    channel_list = requests.get(f'{url}/channels/listall', params={
        'token': users['user3']['token'],
    }).json()

    assert channel_list['channels'][0]['name'] == 'Hello World!'
    assert channel_list['channels'][1]['name'] == 'Hello World!'
    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']

def test_channels_create_invalid_token(url, initialise_user_data):
    '''
    Attempting to call channels_listall without a valid token
    '''
    users = initialise_user_data

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['user0']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    # Checking that AccessError is thrown
    assert requests.post(f'{url}/channels/create', json={
        'token': invalid_token,
        'name': 'Name',
        'is_public': True,
    }).status_code == 400

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
-> APP.route("/channels/list", methods=['GET']) return
   json.dumps({channels})
-> APP.route("/channels/create", methods=['POST']) return
   json.dumps({channel_id})
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
Error type: AccessError
    -> Invalid token
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_channels_list_valid_single(url, initialise_user_data):
    '''
    Listing a single created channel
    '''
    users = initialise_user_data

    # Creating a basic public channel
    channel_id = requests.post(f'{url}/channels/create', json={
        'token': users['user0']['token'],
        'name': 'A Basic Channel',
        'is_public': True,
    }).json()

    # Checking channels_list return is correct
    channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user0']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'A Basic Channel'

    # Type checking
    assert isinstance(channel_list['channels'][0]['channel_id'], int)
    assert isinstance(channel_list['channels'][0]['name'], str)

def test_channels_list_valid_same(url, initialise_user_data):
    '''
    Listing multiple created channels from the same user
    '''
    users = initialise_user_data

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
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': '3rd Channel',
        'is_public': True,
    }).json())

    # Checking channels_list return is correct
    channel_list = requests.get(f'{url}/channels/list', params={
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

def test_channels_list_valid_different(url, initialise_user_data):
    '''
    Listing multiple created channels from different users
    '''
    users = initialise_user_data

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
        'token': users['user3']['token'],
        'name': 'Discussion',
        'is_public': True,
    }).json())

    # Checking channels_list return is correct
    user1_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user1']['token'],
    }).json()
    user2_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user2']['token'],
    }).json()
    user3_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user3']['token'],
    }).json()

    # Id checks
    assert user1_channel_list['channels'][0]['channel_id'] == channel_id[0]['channel_id']
    assert user2_channel_list['channels'][0]['channel_id'] == channel_id[1]['channel_id']
    assert user3_channel_list['channels'][0]['channel_id'] == channel_id[2]['channel_id']

    # Name checks
    assert user1_channel_list['channels'][0]['name'] == 'First Channel'
    assert user2_channel_list['channels'][0]['name'] == 'Channel 2'
    assert user3_channel_list['channels'][0]['name'] == 'Discussion'

def test_channels_list_valid_private(url, initialise_user_data):
    '''
    Listing multiple created private channels from different users
    '''
    users = initialise_user_data

    # Creating channels and storing ids
    channel_id = []

    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'First Channel',
        'is_public': False,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'Channel 2',
        'is_public': False,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': 'Discussion',
        'is_public': False,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': 'Chatter',
        'is_public': False,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user2']['token'],
        'name': '3rd Channel',
        'is_public': False,
    }).json())

    # Checking channels_list return is correct
    user1_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user1']['token'],
    }).json()
    user2_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user2']['token'],
    }).json()

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

def test_channels_list_valid_mix(url, initialise_user_data):
    '''
    Listing a mix of multiple public and private channels from different users with some sharing names
    '''
    users = initialise_user_data

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
        'token': users['user3']['token'],
        'name': 'Discussion',
        'is_public': True,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user1']['token'],
        'name': 'First Channel',
        'is_public': False,
    }).json())
    channel_id.append(requests.post(f'{url}/channels/create', json={
        'token': users['user3']['token'],
        'name': 'Channel 2',
        'is_public': False,
    }).json())

    # Checking channels_list return is correct
    user1_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user1']['token'],
    }).json()
    user2_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user2']['token'],
    }).json()
    user3_channel_list = requests.get(f'{url}/channels/list', params={
        'token': users['user3']['token'],
    }).json()

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

def test_channels_list_valid_empty(url, initialise_user_data):
    '''
    Listing channels when none have been created
    '''
    users = initialise_user_data

    # Checking channels_list return is correct
    assert requests.get(f'{url}/channels/listall', params={
        'token': users['user1']['token'],
    }).json() == {'channels': []}

def test_channels_list_invalid_token(url, initialise_user_data):
    '''
    Attempting to call channels_list without a valid token
    '''
    users = initialise_user_data

    # Only way to guarrantee a token is invalid is to invalidate an existing token
    invalid_token = users['user0']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    # Checking that AccessError is thrown
    assert requests.get(f'{url}/channels/list', params={
        'token': invalid_token,
    }).status_code == 400
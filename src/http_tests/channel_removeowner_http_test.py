'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

Iteration 2
'''

import json
import requests
import pytest
import helper
from error import InputError, AccessError

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

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_http_channel_removeowner_noerrors(initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': 'ch_name0',
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token1,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id1, channel_id)

    # user0 adds user1 as owner
    requests.post(f"{url}/channel/addowner", json={
        'token': token0,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    assert helper.is_channel_owner(u_id1, channel_id)

    # user0 removes user1 as owner
    requests.post(f"{url}/channel/removeowner", json={
        'token': token0,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    assert not helper.is_channel_owner(u_id1, channel_id)

def test_http_channel_removeowner_invalidchannel(initialise_user_data, url):
    '''
    test that channel_removeowner raises InputError if channel_id is not a valid channel_id
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': 'ch_name0',
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token1,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id1, channel_id)

    # user0 adds user1 as owner
    requests.post(f"{url}/channel/addowner", json={
        'token': token0,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    assert helper.is_channel_owner(u_id1, channel_id)

    # assume -1 is not a valid channel id
    channel_id = -1

    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/removeowner", json={
            'token': token0,
            'channel_id': channel_id,
            'u_id': u_id1
        })

def test_http_channel_removeowner_notowner(initialise_user_data, url):
    '''
    test that channel_removeowner raises InputError
    if user with provided u_id is not an owner of the channel
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': 'ch_name0',
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token1,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id1, channel_id)

    # user0 adds user1 as owner
    requests.post(f"{url}/channel/addowner", json={
        'token': token0,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    assert helper.is_channel_owner(u_id1, channel_id)

    # user0 removes user1 as owner
    requests.post(f"{url}/channel/removeowner", json={
        'token': token0,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    assert not helper.is_channel_owner(u_id1, channel_id)

    # attempt to remove owner twice
    # assert that channel_removeowner raises InputError
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/removeowner", json={
            'token': token0,
            'channel_id': channel_id,
            'u_id': u_id1
        })

def test_http_channel_removeowner_authnotowner(initialise_user_data, url):
    '''
    test that channel_removeowner raises AccessError
    if the authorised user is not an owner of the channel or admin of the flockr
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }
    user1_details = requests.post(f"{url}/auth/register", json=user1).json()
    u_id1, token1 = user1_details['u_id'], user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': 'ch_name0',
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token1,
        'channel_id': channel_id
    })

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/removeowner", json={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })

def test_http_channel_removeowner_accesserror(initialise_user_data, url):
    '''
    test that channel_removeowner raises AccessError
    if the authorised user is not an owner of the channel or the flockr
    i.e. test that channel_removeowner raises AccessError if token is invalid
    '''

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }
    user0_details = requests.post(f"{url}/auth/register", json=user0).json()
    u_id0, token0 = user0_details['u_id'], user0_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = requests.post(f"{url}/channels/create", json={
        'token': token0,
        'name': 'ch_name0',
        'is_public': True
    }).json()
    channel_id = channel_info['channel_id']

    # assume " " is always an invalid token
    token0 = " "

    # assert that channel_removeowner raises AccessError
    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/removeowner", json={
            'token': token0,
            'channel_id': channel_id,
            'u_id': u_id0
        })

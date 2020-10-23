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

def test_http_channel_addowner_noerrors(initialise_channel_data, initialise_user_data, url):
    '''
    basic test with no edge case or errors raised
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    token_admin = admin['token']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    u_id0, token0 = user0['u_id'], user0['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user0 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id0, channel_id)

    # admin adds user0 as owner
    requests.post(f"{url}/channel/addowner", json={
        'token': token_admin,
        'channel_id': channel_id,
        'u_id': u_id0
    })

    assert helper.is_channel_owner(u_id0, channel_id)

def test_http_channel_addowner_invalidchannel(initialise_channel_data, initialise_user_data, url):
    '''
    test that channel_addowner raises InputError if channel_id is not a valid channel_id
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    token_admin = admin['token']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    u_id0, token0 = user0['u_id'], user0['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user0 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id0, channel_id)

    # assume -1 is not a valid channel_id
    channel_id = -1

    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/addowner", json={
            'token': token_admin,
            'channel_id': channel_id,
            'u_id': u_id0
        })

def test_http_channel_addowner_alreadyowner(initialise_channel_data, initialise_user_data, url):
    '''
    test that channel_addowner raises InputError
    if user with provided u_id is already an owner of the channel
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    token_admin = admin['token']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    u_id0, token0 = user0['u_id'], user0['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user0 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })
    assert not helper.is_channel_owner(u_id0, channel_id)

    # admin adds user0 as owner
    requests.post(f"{url}/channel/addowner", json={
        'token': token_admin,
        'channel_id': channel_id,
        'u_id': u_id0
    })

    assert helper.is_channel_owner(u_id0, channel_id)

    # attempt to add owner twice
    # assert that channel_addowner raises InputError
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/addowner", json={
            'token': token_admin,
            'channel_id': channel_id,
            'u_id': u_id0
        })

def test_http_channel_addowner_authnotowner(initialise_channel_data, initialise_user_data, url):
    '''
    test that channel_addowner raises AccessError
    if the authorised user is not an owner of the channel
    '''

    # 'admin_publ' is a channel created by the user 'admin'
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # user 'user0' is not admin
    user0 = initialise_user_data['user0']
    u_id0, token0 = user0['u_id'], user0['token']

    # user0 joins channel, therefore is a member but not an owner
    requests.post(f"{url}/channel/join", json={
        'token': token0,
        'channel_id': channel_id
    })

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/addowner", json={
            'token': token0,
            'channel_id': channel_id,
            'u_id': u_id0
        })

def test_http_channel_addowner_invalidtoken(initialise_channel_data, initialise_user_data, url):
    '''
    test that channel_addowner raises AccessError if the provided token is not valid
    '''

    # user 'admin' is the first to register, thus also admin of the flockr
    admin = initialise_user_data['admin']
    u_id_admin, token_admin = admin['u_id'], admin['token']

    # 'admin_publ' is a channel created by the user 'admin', thus 'admin' is a member and owner
    channel_info = initialise_channel_data['admin_publ']
    channel_id = channel_info['channel_id']

    # assume " " is always an invalid token
    token_admin = " "

    # assert that channel_addowner raises AccessError
    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/addowner", json={
            'token': token_admin,
            'channel_id': channel_id,
            'u_id': u_id_admin
        })

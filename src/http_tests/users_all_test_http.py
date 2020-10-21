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
-> APP.route("/users/all", methods=['GET']) return json.dumps({users})
-> APP.route("/auth/logout", methods=['POST']) return json.dumps({is_success})
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
def users_all_initialise_users(url):
    '''
    Sets up various user sample data for testing purposes
    '''

    # Register users:
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


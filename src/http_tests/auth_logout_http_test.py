'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

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
-> APP.route("/auth/logout", methods=['POST']) return
   json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")
   
def test_successful_logout(url, initialise_user_data):
    '''
    Tests that App.route("/auth/logout", methods=['POST']) returns True
    on successful logout
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

def test_active_token_now_invalid(url, initialise_user_data):
    '''
    Tests that App.route("/auth/logout", methods=['POST']) returns True
    on successful logout the first time, but second time when the same
    token is passed it raises an AccessError
    '''
 
    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    logout_again_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_again_response.status_code == 400

def test_invalid_token(url, initialise_user_data):
    '''
    Tests that App.route("/auth/logout", methods=['POST']) raises an
    AccessError when an invalid token is passed as one of the parameters
    '''

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': 'invalid_token'
    })
    assert logout_response.status_code == 400

def test_whitespace_as_token(url, initialise_user_data):
    '''
    Tests that App.route("/auth/logout", methods=['POST']) raises an
    AccessError when a whitespace is passed as token
    '''

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': ' '
    })
    assert logout_response.status_code == 400

def test_return_type(url, initialise_user_data):
    '''
    Tests that App.route("/auth/logout", methods=['POST']) returns the
    expected datatype i.e. { is_success : boolean }
    '''
    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200
    logout_payload = logout_response.json()
    
    assert isinstance(logout_payload, dict)
    assert isinstance(logout_payload['is_success'], bool)

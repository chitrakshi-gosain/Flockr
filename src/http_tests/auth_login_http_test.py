'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import time
import requests

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/auth/login", methods=['POST']) return
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
Error type: InputError
    -> email entered is not a valid email
    -> email entered does not belong to a user
    -> password is not correct
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_successful_login_with_everything_valid(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) logs-in  the
    user successfully
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login_response.status_code == 200

def test_invalid_email(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) raises an
    InputError when an invalid email-id is passed as one of the
    parameters
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0_email.com',
        'password': 'user0_pass1!'
    })
    assert login_response.status_code == 400

def test_unregistered_user(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) raises an
    InputError when an unregistered user tries to log-in
    '''

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user00@email.com',
        'password': 'user0_pass1!'
    })
    assert login_response.status_code == 400

def test_wrong_password(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) raises an
    InputError when a wrong password is passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_Pass1!'
    })
    assert login_response.status_code == 400

def test_return_type(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) returns the expected datatype i.e.
    {u_id : int, token : str}
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login_response.status_code == 200
    login_payload = login_response.json()

    assert isinstance(login_payload, dict)
    assert isinstance(login_payload['u_id'], int)
    assert isinstance(login_payload['token'], str)

def test_login_u_id(url, initialise_user_data):
    '''
    Tests that App.route("/auth/register", methods=['POST']) and
    App.route("/auth/login", methods=['POST']) return same values of
    token and u_id, as there may be a slightest possibility that token
    or u_id of the user might be played around with
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'

    })
    assert login_response.status_code == 200
    login_payload = login_response.json()

    assert login_payload['u_id'] == test_user_0['u_id']

def test_login_unique_token_and_u_id(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) returns a
    unique u_id and token for each user
    '''

    test_user_0 = initialise_user_data['user0']
    logout0_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout0_response.status_code == 200
    login0_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login0_response.status_code == 200
    login0_payload = login0_response.json()

    test_user_1 = initialise_user_data['user0']
    logout1_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_1['token']
    })
    assert logout1_response.status_code == 200
    login1_response = requests.post(f"{url}/auth/login", json={
        'email': 'user1@email.com',
        'password': 'user1_pass1!'
    })
    assert login1_response.status_code == 200
    login1_payload = login1_response.json()

    assert login0_payload != login1_payload
    tokens = [login0_payload['token'], login1_payload['token']]
    assert len(set(tokens)) == len(tokens)

def test_looking_for_negative_u_id(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) does not
    return a negative u_id for a user
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login_response.status_code == 200
    login_payload = login_response.json()

    assert login_payload['u_id'] >= 0

def test_non_ascii_password(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) does not
    accept a Non-ASCII password as one the parameters passed to it
    '''

    test_user_0 = initialise_user_data['user0']

    logout_response = requests.post(f"{url}/auth/logout", json={
        'token': test_user_0['token']
    })
    assert logout_response.status_code == 200

    login_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0\nPass1!'
    })
    assert login_response.status_code == 400

def test_multiple_login_different_tokne(url, initialise_user_data):
    '''
    Tests that App.route("/auth/login", methods=['POST']) allows
    multiple logins, and each login session has a unique token
    '''

    login0_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login0_response.status_code == 200
    login0_payload = login0_response.json()

    time.sleep(5)

    login1_response = requests.post(f"{url}/auth/login", json={
        'email': 'user0@email.com',
        'password': 'user0_pass1!'
    })
    assert login1_response.status_code == 200
    login1_payload = login1_response.json()

    assert login0_payload != login1_payload
    tokens = [login0_payload['token'], login1_payload['token']]
    assert len(set(tokens)) == len(tokens)

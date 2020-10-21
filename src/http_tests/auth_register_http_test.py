'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import json
import requests
import pytest
from error import InputError
from auth import auth_register

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
'''

'''
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> email entered is not a valid email
    -> email address is already being used by another user
    -> password entered is less than 6 characters long or more than 32
       characters long
    -> name_first is not between 1 and 50 characters inclusively in
       length
    -> name_last is not between 1 and 50 characters inclusively in
       length
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_successful_registration(url, reset):
    '''
    Tests that App.route("/auth/register", methods=['POST']) registers a
    new user successfully
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_invalid_email(url, reset):
    '''
    Tests that auth_register raises an InputError when an invalid email
    is passed as one of the parameters
    '''

    user0 = {
        'email': 'user0_email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_existing_email_registration(url, reset):
    '''
    Tests that auth_register raises an InputError when a user tries to
    register with an existing email-id in database registered with
    another user
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response_1 = requests.post(f"{url}/auth/register", json=user0).json()
    assert response_1.status_code == 200

    response_2 = requests.post(f"{url}/auth/register", json=user0).json()
    assert response_2.status_code == 400

def test_too_short_first_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    less than 1 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': '',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_too_long_first_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    more than 50 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first' * 5,
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_too_short_last_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_last is
    less than 1 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': ''
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_too_long_last_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_last is
    more than 50 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last' * 5
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_password_too_short_(url, reset):
    '''
    Tests that auth_register raises an InputError when a password is
    less than 6 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_password_too_long_(url, reset):
    '''
    Tests that auth_register raises an InputError when a password is
    more than 32 characters long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*7',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_insufficient_parameters(url, reset):
    '''
    Tests that auth_login raises an InputError when less than expected
    parameters are passed
    '''
    user0 = {
        'email': 'user0@email.com',
        'password': None,
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_return_type(url, reset):
    '''
    Tests that auth_register returns the expected datatype i.e.
    {u_id : int, token : str}
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert payload.status_code == 200
    assert isinstance(payload['u_id'], int)
    assert isinstance(payload['token'], str)

def test_non_ascii_name_first(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    Non-ASCII
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'Anaïs',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0)
    assert response.status_code == 400

def test_non_ascii_name_last(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_last is
    Non-ASCII
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'सिंह'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_looking_for_negative_u_id(url, reset):
    '''
    Tests that auth_register does not return a negative u_id
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    payload = requests.post(f"{url}/auth/register", json=user0).json()
    # payload = response.json()
    # assert response.status_code == 200
    assert payload.status_code == 200
    assert payload['u_id'] >= 0

def test_non_ascii_password(url, reset):
    '''
    Tests that auth_register raises an InputError when a password is
    Non-ASCII
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0 \n pass1!',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_whitespace_first_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': '    ',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_whitespace_last_name(url, reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': '    '
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 400

def test_lowercase_handle(url, reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }

    auth_payload = requests.post(f"{url}/auth/register", json=user0).json()
    # auth_payload = auth_response.json()
    # assert auth_response.status_code == 200
    assert auth_payload.status_code == 200

    # user0_credentials = {
    #     'token': auth_payload['token'],
    #     'u_id': auth_payload['u_id']
    # }

    user_payload = requests.get(f"{url}/user/profile", params=auth_payload).json()
    # user_payload = user_response.json()
    # assert user_response.status_code == 200
    assert user_payload.status_code == 200
    assert user_payload['user']['handle_str'] == 'user0_firstuser0_las'

def test_unique_handle(url, reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. Each user has valid and
    different handle
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }

    auth0_payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert auth0_payload.status_code == 200

    user0_payload = requests.get(f"{url}/user/profile", params=auth0_payload).json()
    assert user0_payload.status_code == 200

    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_FIRST',
        'name_last': 'user1_LAST'
    }

    auth1_payload = requests.post(f"{url}/auth/register", json=user1).json()
    assert auth1_payload.status_code == 200

    user1_payload = requests.get(f"{url}/user/profile", params=auth1_payload).json()
    assert user1_payload.status_code == 200

    assert user0_payload['user']['handle_str'] != user1_payload['user']\
        ['handle_str']

def test_too_long_handle_first_name(url, reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST' * 2,
        'name_last': 'user0_LAST'
    }

    auth_payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert auth_payload.status_code == 200

    user_payload = requests.get(f"{url}/user/profile", params=auth_payload).json()
    assert user_payload.status_code == 200
    assert user_payload['user']['handle_str'] == 'user0_firstuser0_fir'

def test_too_long_handle_last_name(url, reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'u',
        'name_last': 'user0_LAST' * 2
    }

    auth_payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert auth_payload.status_code == 200

    user_payload = requests.get(f"{url}/user/profile", params=auth_payload).json()
    assert user_payload.status_code == 200
    assert user_payload['user']['handle_str'] == 'uuser0_lastuser0_las'

def test_handle_for_users_with_similar_first_last_names(url, reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. For a new user with
    similar name_first and name_last as one/more existing users there is
    some modification to new user's handle
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }
    auth0_payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert auth0_payload.status_code == 200
    user0_payload = requests.get(f"{url}/user/profile", params=auth0_payload).json()
    assert user0_payload.status_code == 200

    user1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass1!',
        'name_first': 'user1_FIRST',
        'name_last': 'user1_LAST'
    }
    auth1_payload = requests.post(f"{url}/auth/register", json=user1).json()
    assert auth1_payload.status_code == 200
    user1_payload = requests.get(f"{url}/user/profile", params=auth1_payload).json()
    assert user1_payload.status_code == 200

    user2 = {
        'email': 'user2@email.com',
        'password': 'user2_pass1!',
        'name_first': 'user2_FIRST',
        'name_last': 'user2_LAST'
    }
    auth2_payload = requests.post(f"{url}/auth/register", json=user2).json()
    assert auth2_payload.status_code == 200
    user2_payload = requests.get(f"{url}/user/profile", params=auth2_payload).json()
    assert user2_payload.status_code == 200

    user3 = {
        'email': 'user3@email.com',
        'password': 'user3_pass1!',
        'name_first': 'user3_FIRST',
        'name_last': 'user3_LAST'
    }
    auth3_payload = requests.post(f"{url}/auth/register", json=user3).json()
    assert auth3_payload.status_code == 200
    user3_payload = requests.get(f"{url}/user/profile", params=auth3_payload).json()
    assert user3_payload.status_code == 200

    assert user0_payload['user']['handle_str'] != user2_payload['user']\
        ['handle_str']
    assert user1_payload['user']['handle_str'] != user3_payload['user']\
        ['handle_str']

def test_first_name_1_char(url, reset):
    '''
    Tests that auth_register accepts a name_first which is 1 character
    long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'u',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_first_name_50_chars(url, reset):
    '''
    Tests that auth_register accepts a name_first which is 50 characters
    long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'u' * 50,
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_last_name_1_char(url, reset):
    '''
    Tests that auth_register accepts a name_last which is 1 character
    long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'u'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_last_name_50_chars(url, reset):
    '''
    Tests that auth_register accepts a name_last which is 50 characters
    long
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_first',
        'name_last': 'u' * 50
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_password_6_chars(url, reset):
    '''
    Tests that auth_register accepts a password which is 6 characters
    long
    '''


    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_',
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

    auth_register('user0@email.com', 'user0_', 'user0_first', 'user0_last')

def test_password_32_chars(url, reset):
    '''
    Tests that auth_register accepts a password which is 32 characters
    long
    '''


    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_password1!' * 2,
        'name_first': 'user0_first',
        'name_last': 'user0_last'
    }

    response = requests.post(f"{url}/auth/register", json=user0).json()
    assert response.status_code == 200

def test_details_registered_by_auth_register(url, reset):
    '''
    Tests that auth_register has stored all the general details of a
    user correctly
    '''

    user0 = {
        'email': 'user0@email.com',
        'password': 'user0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }
    auth_payload = requests.post(f"{url}/auth/register", json=user0).json()
    assert auth_payload.status_code == 200
    user_payload = requests.get(f"{url}/user/profile", params=auth_payload).json()
    assert user_payload.status_code == 200
    assert user_payload == {
        'user': {
            'u_id': auth_payload['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las'
        }
    }

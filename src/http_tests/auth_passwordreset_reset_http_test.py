'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import json
import requests
import pytest

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_FOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route(.....) return json.dumps({...})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
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

def test_invalid_reset_code(url, reset):
    '''
    ADD DOCSTRING HERE
    '''

    reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': ' ',
        'new_password': 'some_password'
    })
    print(reset_response.json())
    assert reset_response.status_code == 400

def test_new_password_too_short(url, initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user0@email.com'
    })
    assert resetrequest_response.status_code == 200

    reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': 'reset_code',
        'new_password': 'some'
    })
    assert reset_response.status_code == 400

# commenting till i figure out a way to suppress and record emails and finally retrieve reset_code from them
# def test_new_password_too_long(url, initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
#         'email': 'user0@email.com'
#     })
#     assert resetrequest_response.status_code == 200

#     reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
#         'reset_code': 'reset_code',
#         'new_password': 'some' * 10
#     })
#     assert reset_response.status_code == 400

# def test_new_password_is_actually_old(url, initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
#         'email': 'user0@email.com'
#     })
#     assert resetrequest_response.status_code == 200

#     reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
#         'reset_code': 'reset_code',
#         'new_password': 'user0_pass1!'
#     })
#     assert reset_response.status_code == 200

# def test_successful_reset(url, initialise_user_data):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
#         'email': 'user0@email.com'
#     })
#     assert resetrequest_response.status_code == 200

#     reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
#         'reset_code': 'reset_code',
#         'new_password': 'user0_password1!'
#     })
#     assert reset_response.status_code == 200

# def test_return_type(url, initialise_user_data):
#     resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
#         'email': 'user0@email.com'
#     })
#     assert resetrequest_response.status_code == 200

#     reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
#         'reset_code': 'reset_code',
#         'new_password': 'user0_password1!'
#     })
#     assert reset_response.status_code == 200
#     reset_payload = reset_response.json()

#     assert not reset_payload

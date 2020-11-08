'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import json
import requests
import pytest
from server import APP

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/auth/passwordreset/request", methods=['POST']) return
   json.dumps({})
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

APP.config['TESTING'] = True
# technically i should reinstatiate the mail object, but i'm not passing
# the mail object as an argument so how do i do it? this will still send email :(

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_invalid_email(url, reset):
    '''
    Tests that App.route("/auth/passwordreset/request", methods=['POST'])
    raises an InputError when an invalid email-id is passed as one of
    the parameters
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request",\
        json={
        'email': 'user0_email.com'
    })

    assert resetrequest_response.status_code == 400

def test_unregistered_user(url, reset):
    '''
    Tests that App.route("/auth/passwordreset/request", methods=['POST'])
    raises an InputError when an unregistered user tries to request for
    a reset code to change his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request",\
        json={
        'email': 'user00@email.com'
    })

    assert resetrequest_response.status_code == 400

def test_reset_code_sent_successfully(url, initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully send an email to
    the user with reset code so that he can reset his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'chitrakshi6072@gmail.com'
    })

    assert resetrequest_response.status_code == 200

def test_return_type(url, initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully returns the reset
    code which is of string type as per the spec
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'chitrakshi6072@gmail.com'
    })
    # assert resetrequest_response.status_code == 200
    resetrequest_payload = resetrequest_response.json()

    assert not resetrequest_payload

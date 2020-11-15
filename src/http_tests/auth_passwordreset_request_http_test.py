'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 3
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
-> APP.route("/auth/passwordreset/request", methods=['POST']) return
   json.dumps({})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError]
    -> email entered is not a valid email
    -> email entered does not belong to a user
'''

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

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user0_email.com'
    })

    assert resetrequest_response.status_code == 400

def test_unregistered_user(url, reset):
    '''
    Tests that App.route("/auth/passwordreset/request", methods=['POST'])
    raises an InputError when an unregistered user tries to request for
    a reset code to change his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user00@email.com'
    })

    assert resetrequest_response.status_code == 400

def test_reset_code_sent_successfully(url, initialise_user_data):
    '''
    Tests that APP.route("/auth/passwordreset/request", methods=['POST'])
    successfully send an email to the user with reset code so that he
    can reset his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user0@email.com'
    })

    assert resetrequest_response.status_code == 200

def test_return_type(url, initialise_user_data):
    '''
    Tests that APP.route("/auth/passwordreset/request", methods=['POST'])
    successfully returns the reset code which is of string type as per
    the spec
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user0@email.com'
    })
    assert resetrequest_response.status_code == 200
    resetrequest_payload = resetrequest_response.json()

    assert not resetrequest_payload

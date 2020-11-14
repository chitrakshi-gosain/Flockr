'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Huynh

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
-> APP.route("/clear", methods=['DELETE']) return json.dumps({})
-> APP.route("/auth/logout") return json.dumps({})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
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

def test_clear(url):
    '''
    tests clear by searching for a now deleted token which then throws error
    '''

    register_input = {"email": "admin@flockr.com", "password": "itsasecret",
                    "name_first": "adminfirst", "name_last": "adminlast"}
    register_output = requests.post(url + "/auth/register", json=register_input).json()

    valid_token = register_output['token']

    requests.delete(url + "/clear")
    #now valid_token is invalid (expect error)
    logout_input = {"token": valid_token}
    logout_output = requests.post(url + "/auth/logout", json=logout_input)

    assert logout_output.status_code == 400

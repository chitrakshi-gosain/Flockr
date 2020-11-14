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
APP.routes_USED_FOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/auth/passwordreset/request", methods=['POST']) return
   json.dumps({})
-> APP.route("/auth/passwordreset/reset", methods=['POST']) return
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
Error type: InputError
    -> reset_code is not a valid reset_code
    -> password entered is not a valid password
    -> password entered is similar to one of the old passwords
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_invalid_reset_code(url, reset):
    '''
    Tests that APP.route("/auth/passwordreset/reset", methods=['POST'])
    raises an AccessError when an invalid reset code is passed as one of
    the parameters
    '''

    reset_response = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': ' ',
        'new_password': 'some_password'
    })
    print(reset_response.json())
    assert reset_response.status_code == 400

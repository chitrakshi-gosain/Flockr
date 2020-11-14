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

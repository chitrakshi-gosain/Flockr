'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Ahmet Karatas

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
-> APP.route("/message/send", methods=['POST']) return
    json.dumps({token, channel_id, message})
-> APP.route("/message/pin", methods=['POST']) return
    json.dumps({})
-> APP.route("/channel/join", methods=['POST']) return json.dumps({})
-> APP.route("/auth/register", methods=['POST']) return
    json.dumps({u_id, token})
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error Type: InputError
    -> token is invalid
    -> Message is already pinned
    -> message_id given is not a valid message_Id
Error Type: AccessError
    -> User is not an authorised member of the channel which contains the message
    -> The user is not an owner
'''
def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")


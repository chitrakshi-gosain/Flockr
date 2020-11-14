'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Joseph Knox

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
-> APP.route("/channels/create", methods=['POST']) return
    json.dumps({channel_id})
-> APP.route("/user/profile", methods=['GET']) return
    json.dumps({user})
-> APP.route("/user/profile/setname", methods=['PUT']) return
    json.dumps({})
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
Error type: InputError
    -> length of name_first is <1 or >50
    -> length of name_last is <1 or >50
Error type: AccessError
    -> token is not valid
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")


def test_http_user_profile_setname_no_errors(url, initialise_user_dictionary, initialise_user_data):
    '''
    basic test with no edge case or errors raised
    '''

    user_details = initialise_user_data['user0']
    user_dict = initialise_user_dictionary['user0_dict']

    user_profile_response = requests.get(f"{url}/user/profile", params={
        'token': user_details['token'],
        'u_id': user_details['u_id']
    })
    assert user_profile_response.status_code == 200
    user_profile_info = user_profile_response.json()

    assert user_profile_info['user']['name_first'] == user_dict['name_first']
    assert user_profile_info['user']['name_last'] == user_dict['name_last']

    user_setname = requests.put(f"{url}/user/profile/setname", json={
        'token': user_details['token'],
        'name_first': 'name_first_new',
        'name_last': 'name_last_new'
    })
    assert user_setname.status_code == 200

    user_profile_response1 = requests.get(f"{url}/user/profile", params={
        'token': user_details['token'],
        'u_id': user_details['u_id']
    })
    assert user_profile_response1.status_code == 200
    user_profile_info1 = user_profile_response1.json()

    assert user_profile_info1['user']['name_first'] == 'name_first_new'
    assert user_profile_info1['user']['name_last'] == 'name_last_new'


def test_http_user_profile_setname_inputerror(url, initialise_user_dictionary, initialise_user_data):
    '''
    test that user_profile_setname raises InputError
    if provided name_first or name_last is not between 1 and 50 characters in length
    '''

    user_details = initialise_user_data['user0']
    user_dict = initialise_user_dictionary['user0_dict']

    user_profile_response = requests.get(f"{url}/user/profile", params={
        'token': user_details['token'],
        'u_id': user_details['u_id']
    })
    assert user_profile_response.status_code == 200
    user_profile_info = user_profile_response.json()

    assert user_profile_info["user"]['name_first'] == user_dict['name_first']
    assert user_profile_info["user"]['name_last'] == user_dict['name_last']

    setname_response0 = requests.put(f"{url}/user/profile/setname", json={
            'token': user_details['token'],
            'name_first': '',
            'name_last': 'name_last_new'
    })
    assert setname_response0.status_code == 400

    setname_response1 = requests.put(f"{url}/user/profile/setname", json={
            'token': user_details['token'],
            'name_first': 'name_first_new',
            'name_last': ''
    })
    assert setname_response1.status_code == 400

    setname_response2 = requests.put(f"{url}/user/profile/setname", json={
            'token': user_details['token'],
            'name_first': 'name_first_new',
            'name_last': '123456789012345678901234567890123456789012345678901'
    })
    assert setname_response2.status_code == 400

    setname_response3 = requests.put(f"{url}/user/profile/setname", json={
            'token': user_details['token'],
            'name_first': '123456789012345678901234567890123456789012345678901',
            'name_last': 'name_last_new'
    })
    assert setname_response3.status_code == 400

def test_http_user_profile_setname_accesserror(url, initialise_user_dictionary, initialise_user_data):
    '''
    test that user_profile_setname raises AccessError
    if provided token is invalid
    '''

    user_details = initialise_user_data['user0']
    user_dict = initialise_user_dictionary['user0_dict']

    user_profile_response = requests.get(f"{url}/user/profile", params={
        'token': user_details['token'],
        'u_id': user_details['u_id']
    })
    assert user_profile_response.status_code == 200
    user_profile_info = user_profile_response.json()

    assert user_profile_info['user']['name_first'] == user_dict['name_first']
    assert user_profile_info['user']['name_last'] == user_dict['name_last']

    setname_response = requests.put(f"{url}/user/profile/setname", json={
            'token': " ",
            'name_first': 'name_first_new',
            'name_last': 'name_last_new'
    })
    assert setname_response.status_code == 400

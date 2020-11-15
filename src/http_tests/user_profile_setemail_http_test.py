'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

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
-> APP.route("/user/profile", methods=['GET']) return
   json.dumps({user})
-> APP.route("/user/profile/setemail", methods=['PUT']) return
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
    -> email entered is not a valid email
    -> email address is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_return_type(url, initialise_user_data):
    '''
    Tests that user_profile_setemail returns the expected datatype i.e.
    {}
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user0newemailid@email.com'
    })
    assert update_response.status_code == 200
    update_email_payload = update_response.json()
    assert isinstance(update_email_payload, dict)
    assert not update_email_payload

def test_invalid_token(url, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an AccessError when an
    invalid token is passed as one of the parameters
    '''

    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': 'invalid_token',
        'email': 'user0newemailid@email.com'
    })
    assert update_response.status_code == 400

def test_invalid_email(url, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when an
    invalid email is passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user0newemailid_email.com'
    })
    assert update_response.status_code == 400

def test_existing_email(url, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when a user
    tries to update his email-id to an existing email-id in database
    registered with another user
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user1@email.com'
    })
    assert update_response.status_code == 400

def test_successful_email_updatation(url, initialise_user_data):
    '''
    Tests that user_profile_setemail updates email-id of a user to an
    email-id entered by user, if it does not exist in database i.e. it
    is not being used by any registered user at that instance
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user0newemailid@email.com'
    })
    assert update_response.status_code == 200

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['email'] == 'user0newemailid@email.com'

def test_only_unique_changes_accepted(url, initialise_user_data):
    '''
    Tests that user_profile_setemail accepts to update an email-id which
    previously belonged to another user and is now not a part of the
    database for a different user
    '''

    test_user_0 = initialise_user_data['user0']
    update0_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user0newemailid@email.com'
    })
    assert update0_response.status_code == 200

    profile0_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile0_response.status_code == 200
    user_profile0_payload = profile0_response.json()
    assert user_profile0_payload['user']['email'] == 'user0newemailid@email.com'

    test_user_1 = initialise_user_data['user1']
    update1_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_1['token'],
        'email': 'user0@email.com'
    })
    assert update1_response.status_code == 200

    profile1_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_1['token'],
        'u_id': test_user_1['u_id']
    })
    assert profile1_response.status_code == 200
    user_profile1_payload = profile1_response.json()
    assert user_profile1_payload['user']['email'] == 'user0@email.com'

    assert user_profile0_payload['user']['email'] != user_profile1_payload['user']['email']

def test_no_change(url, initialise_user_data):
    '''
    Tests that user_profile_setemail does not raise an InputError when a
    user tries to update his email-id to an existing email-id in
    database registered with himself
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/setemail", json={
        'token': test_user_0['token'],
        'email': 'user0@email.com'
    })
    assert update_response.status_code == 200
    update_payload = update_response.json()

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['email'] == 'user0@email.com'

    assert user_profile_payload['user']['email'] == 'user0@email.com'
    assert isinstance(update_payload, dict)
    assert not update_payload

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
-> APP.route("/user/profile/sethandle", methods=['PUT']) return
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
    -> handle_str must be between 3 and 20 characters
    -> handle is already being used by another user
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
    Tests that user_profile_sethandle returns the expected datatype i.e.
    {}
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'my_new_handle'
    })
    assert update_response.status_code == 200
    update_handle_payload = update_response.json()
    assert isinstance(update_handle_payload, dict)
    assert not update_handle_payload

def test_invalid_token(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an AccessError when an
    invalid token is passed as one of the parameters
    '''

    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': 'invalid_user_token',
        'handle_str': 'my_new_handle'
    })
    assert update_response.status_code == 400

def test_too_short_handle_str(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a
    handle entered by user for updatation is less than 3 characters
    long
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'me'
    })
    assert update_response.status_code == 400

def test_too_long_handle_str(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a
    handle entered by user for updatation is more than 20 characters
    long
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'my_' * 7
    })
    assert update_response.status_code == 400

def test_successful_handle_updatation(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle updates handle of a user to an
    handle entered by user, if it does not exist in database i.e. it
    is not being used by any registered user at that instance
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'user_0_handle'
    })
    assert update_response.status_code == 200

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'user_0_handle'
    
def test_handle_3_chars(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    is 3 characters long
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'me_'
    })
    assert update_response.status_code == 200

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'me_'

def test_handle_20_chars(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    is 20 characters long
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'hi' * 10
    })
    assert update_response.status_code == 200

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'hi' * 10

def test_non_ascii_handle(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    has Non-ASCII characters
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'âêîôû é àèù ëïü'
    })
    assert update_response.status_code == 200

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'âêîôû é àèù ëïü'

def test_existing_handle(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a user
    tries to update his handle to an existing handle in database
    registered with another user
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'user1_firstuser1_las'
    })
    assert update_response.status_code == 400

def test_whitespace_handle(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a handle
    entered by user for updatation is completely whitespace
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': '        '
    })
    assert update_response.status_code == 400

def test_no_change(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle does not raise an InputError when
    a user tries to update his handle to an existing handle in
    database registered with himself
    '''

    test_user_0 = initialise_user_data['user0']
    update_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'user0_firstuser0_las'
    })
    assert update_response.status_code == 200
    update_payload = update_response.json()

    profile_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile_response.status_code == 200
    user_profile_payload = profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'user0_firstuser0_las'
    assert isinstance(update_payload, dict)
    assert not update_payload

def test_only_unique_changes_accepted(url, initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts to update a handle which
    previously belonged to another user and is now not a part of the
    database for a different user
    '''

    test_user_0 = initialise_user_data['user0']
    update0_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'user_0_handle'
    })
    assert update0_response.status_code == 200

    profile0_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile0_response.status_code == 200
    user_profile0_payload = profile0_response.json()
    assert user_profile0_payload['user']['handle_str'] == 'user_0_handle'

    test_user_0 = initialise_user_data['user0']
    update1_response = requests.put(f"{url}/user/profile/sethandle", json={
        'token': test_user_0['token'],
        'handle_str': 'user0_firstuser0_l'
    })
    assert update1_response.status_code == 200

    profile1_response = requests.get(f"{url}/user/profile", params={
        'token': test_user_0['token'],
        'u_id': test_user_0['u_id']
    })
    assert profile1_response.status_code == 200
    user_profile1_payload = profile1_response.json()
    assert user_profile1_payload['user']['handle_str'] == 'user0_firstuser0_l'

    assert user_profile0_payload['user']['handle_str'] != user_profile1_payload['user']['handle_str']

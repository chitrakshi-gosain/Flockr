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
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> initialise_user_dictionary
'''

'''
EXCEPTIONS
Error type: InputError
    -> email entered is not a valid email
    -> email address is already being used by another user
    -> password entered is less than 6 characters long or more than 32
       characters long
    -> name_first is not between 1 and 50 characters inclusively in
       length
    -> name_last is not between 1 and 50 characters inclusively in
       length
'''

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_successful_registration(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) registers a
    new user successfully
    '''

    user0 = initialise_user_dictionary['user0_dict']
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_invalid_email(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when an invalid email is passed as one of the parameters
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['email'] = 'user0_email.com'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_existing_email_registration(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a user tries to register with an existing email-id
    in database registered with another user
    '''

    user0 = initialise_user_dictionary['user0_dict']
    register_response_1 = requests.post(f"{url}/auth/register", json=user0)
    assert register_response_1.status_code == 200

    register_response_2 = requests.post(f"{url}/auth/register", json=user0)
    assert register_response_2.status_code == 400

def test_too_short_first_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_first is less than 1 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = ''
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_too_long_first_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_first is more than 50 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = 'user0_first' * 5
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_too_short_last_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_last is less than 1 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_last'] = ''
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_too_long_last_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_last is more than 50 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_last'] = 'user0_last' * 6
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_password_too_short_(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a password is less than 6 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['password'] = 'user0'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_password_too_long_(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a password is more than 32 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['password'] = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*7'    
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_return_type(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) returns the
    expected datatype i.e. {u_id : int, token : str}
    '''

    user0 = initialise_user_dictionary['user0_dict']
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200
    payload = register_response.json()
    assert isinstance(payload['u_id'], int)
    assert isinstance(payload['token'], str)

def test_non_ascii_name_first(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) does not
    raise an InputError when a name_first is Non-ASCII
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = 'Anaïs'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_non_ascii_name_last(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) does not
    raise an InputError when a name_last is Non-ASCII
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = 'सिंह'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_looking_for_negative_u_id(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) does not
    return a negative u_id
    '''

    user0 = initialise_user_dictionary['user0_dict']
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200
    payload = register_response.json()
    assert payload['u_id'] >= 0

def test_non_ascii_password(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a password is Non-ASCII
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['password'] = 'user0 \n pass1!'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_whitespace_first_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_first is completely whitespace
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = '    '
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_whitespace_last_name(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) raises an
    InputError when a name_first is completely whitespace
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_last'] = '    '
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 400

def test_lowercase_handle(url):
    '''
    Tests that App.route("/auth/register", methods=['POST'])
    implements handle_str as per specifications, i.e. concatenates
    lowercase name_first and name_last
    '''

    test_user = {
        'email': 'testuser0@email.com',
        'password': 'testuser0_pass1!',
        'name_first': 'user0_FIRST',
        'name_last': 'user0_LAST'
    }

    register_response = requests.post(f"{url}/auth/register", json=test_user)
    assert register_response.status_code == 200
    register_payload = register_response.json()

    user_profile_response = requests.get(f"{url}/user/profile", params=register_payload)
    assert user_profile_response.status_code == 200
    user_profile_payload = user_profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'user0_firstuser0_las'

def test_unique_handle(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST'])
    implements handle_str as per specifications, i.e. concatenates
    lowercase name_first and name_last and cuts it if greater than 20
    characters. Each user has valid and different handle
    '''

    user0 = initialise_user_dictionary['user0_dict']

    auth0_register_response = requests.post(f"{url}/auth/register", json=user0)
    assert auth0_register_response.status_code == 200
    auth0_payload = auth0_register_response.json()

    user0_register_response = requests.get(f"{url}/user/profile", params=auth0_payload)
    assert user0_register_response.status_code == 200
    user0_payload = user0_register_response.json()

    user1 = initialise_user_dictionary['user1_dict']

    auth1_register_response = requests.post(f"{url}/auth/register", json=user1)
    assert auth1_register_response.status_code == 200
    auth1_payload = auth1_register_response.json()

    user1_register_response = requests.get(f"{url}/user/profile", params=auth1_payload)
    assert user1_register_response.status_code == 200
    user1_payload = user1_register_response.json()

    assert user0_payload['user']['handle_str'] != user1_payload['user']\
        ['handle_str']

def test_too_long_handle_first_name(url):
    '''
    Tests that App.route("/auth/register", methods=['POST'])
   implements handle_str as per specifications, i.e. concatenates
    lowercase name_first and name_last and cuts it if greater than 20
    characters
    '''

    test_user = {
        'email': 'testuser0@email.com',
        'password': 'testuser0_pass1!',
        'name_first': 'testuser0_first' * 2 ,
        'name_last': 'testuser0_last'
    }

    register_response = requests.post(f"{url}/auth/register", json=test_user)
    assert register_response.status_code == 200
    register_payload = register_response.json()

    user_profile_response = requests.get(f"{url}/user/profile", params=register_payload)
    assert user_profile_response.status_code == 200
    user_profile_payload = user_profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'testuser0_firsttestu'

def test_too_long_handle_last_name(url):
    '''
    Tests that App.route("/auth/register", methods=['POST'])
    implements handle_str as per specifications, i.e. concatenates
    lowercase name_first and name_last and cuts it if greater than 20
    characters
    '''

    test_user = {
        'email': 'testuser0@email.com',
        'password': 'testuser0_pass1!',
        'name_first': 't',
        'name_last': 'testuser0_last' * 2
    }

    register_response = requests.post(f"{url}/auth/register", json=test_user)
    assert register_response.status_code == 200
    register_payload = register_response.json()

    user_profile_response = requests.get(f"{url}/user/profile", params=register_payload)
    assert user_profile_response.status_code == 200
    user_profile_payload = user_profile_response.json()
    assert user_profile_payload['user']['handle_str'] == 'ttestuser0_lasttestu'

def test_handle_for_users_with_similar_first_last_names(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST'])
    implements handle_str as per specifications, i.e. concatenates
    lowercase name_first and name_last and cuts it if greater than 20
    characters. For a new user with similar name_first and name_last as
    one/more existing users there is some modification to new user's
    handle
    '''

    user0 = initialise_user_dictionary['user0_dict']
    auth0_register_response = requests.post(f"{url}/auth/register", json=user0)
    assert auth0_register_response.status_code == 200
    auth0_payload = auth0_register_response.json()

    user0_register_response = requests.get(f"{url}/user/profile", params=auth0_payload)
    assert user0_register_response.status_code == 200
    user0_payload = user0_register_response.json()

    user1 = initialise_user_dictionary['user1_dict']

    auth1_register_response = requests.post(f"{url}/auth/register", json=user1)
    assert auth1_register_response.status_code == 200
    auth1_payload = auth1_register_response.json()

    user1_register_response = requests.get(f"{url}/user/profile", params=auth1_payload)
    assert user1_register_response.status_code == 200
    user1_payload = user1_register_response.json()

    user2 = initialise_user_dictionary['user2_dict']
    auth2_register_response = requests.post(f"{url}/auth/register", json=user2)
    assert auth2_register_response.status_code == 200
    auth2_payload = auth2_register_response.json()

    user2_register_response = requests.get(f"{url}/user/profile", params=auth2_payload)
    assert user2_register_response.status_code == 200
    user2_payload = user2_register_response.json()

    user3 = initialise_user_dictionary['user3_dict']
    auth3_register_response = requests.post(f"{url}/auth/register", json=user3)
    assert auth3_register_response.status_code == 200
    auth3_payload = auth3_register_response.json()
    user3_register_response = requests.get(f"{url}/user/profile", params=auth3_payload)
    assert user3_register_response.status_code == 200
    user3_payload = user3_register_response.json()

    assert user0_payload['user']['handle_str'] != user2_payload['user']\
        ['handle_str']
    assert user1_payload['user']['handle_str'] != user3_payload['user']\
        ['handle_str']

def test_first_name_1_char(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    name_first which is 1 character long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = 'u'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_first_name_50_chars(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    name_first which is 50 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_first'] = 'u' * 50
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_last_name_1_char(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    name_last which is 1 character long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_last'] = 'u'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_last_name_50_chars(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    name_last which is 50 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['name_last'] = 'u' * 50
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_password_6_chars(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    password which is 6 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['password'] = 'user0_'
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_password_32_chars(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) accepts a
    password which is 32 characters long
    '''

    user0 = initialise_user_dictionary['user0_dict']
    user0['password'] = 'user0_password1!' * 2
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200

def test_details_registered_by_auth_register(url, initialise_user_dictionary):
    '''
    Tests that App.route("/auth/register", methods=['POST']) has
    stored all the general details of a user correctly
    '''

    user0 = initialise_user_dictionary['user0_dict']
    register_response = requests.post(f"{url}/auth/register", json=user0)
    assert register_response.status_code == 200
    register_payload = register_response.json()
    user_profile_response = requests.get(f"{url}/user/profile", params=register_payload)
    assert user_profile_response.status_code == 200
    user_profile_payload = user_profile_response.json()
    assert user_profile_payload == {
        'user': {
            'u_id': register_payload['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las',
            'profile_img_url': '',
        }
    }

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

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
-> APP.route("/users/all", methods=['GET']) return json.dumps({users})
-> APP.route("/auth/logout", methods=['POST']) return json.dumps({is_success})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_users
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

def test_users_all_basic(url, initialise_user_data):
    '''
    Basic valid test case of users_all
    '''
    user_data = initialise_user_data

    all_users = requests.get(f'{url}/users/all', params={
        'token': user_data['user0']['token'],
    }).json()

    exp_dict = {
        'users': [
            {
                'u_id': user_data['admin']['u_id'],
                'email': 'admin@email.com',
                'name_first': 'admin_first',
                'name_last': 'admin_last',
                'handle_str': 'admin_firstadmin_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
                'profile_img_url': '',
            }
        ]
    }

    assert all_users == exp_dict

def test_users_all_logout(url, initialise_user_data):
    '''
    Tests that all user profiles are returned even if
    some users are logged out
    '''
    user_data = initialise_user_data

    requests.post(f'{url}/auth/logout', json={
        'token': user_data['admin']['token'],
    })
    requests.post(f'{url}/auth/logout', json={
        'token': user_data['owner']['token'],
    })

    all_users = requests.get(f'{url}/users/all', params={
        'token': user_data['user3']['token'],
    }).json()

    exp_dict = {
        'users': [
            {
                'u_id': user_data['admin']['u_id'],
                'email': 'admin@email.com',
                'name_first': 'admin_first',
                'name_last': 'admin_last',
                'handle_str': 'admin_firstadmin_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['owner']['u_id'],
                'email': 'owner@email.com',
                'name_first': 'owner_first',
                'name_last': 'owner_last',
                'handle_str': 'owner_firstowner_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user0']['u_id'],
                'email': 'user0@email.com',
                'name_first': 'user0_first',
                'name_last': 'user0_last',
                'handle_str': 'user0_firstuser0_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user1']['u_id'],
                'email': 'user1@email.com',
                'name_first': 'user1_first',
                'name_last': 'user1_last',
                'handle_str': 'user1_firstuser1_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user2']['u_id'],
                'email': 'user2@email.com',
                'name_first': 'user2_first',
                'name_last': 'user2_last',
                'handle_str': 'user2_firstuser2_las',
                'profile_img_url': '',
            },
            {
                'u_id': user_data['user3']['u_id'],
                'email': 'user3@email.com',
                'name_first': 'user3_first',
                'name_last': 'user3_last',
                'handle_str': 'user3_firstuser3_las',
                'profile_img_url': '',
            }
        ]
    }

    assert all_users == exp_dict

def test_users_all_invalid_token(url, initialise_user_data):
    '''
    Testing users_all with an invalid token parameter
    '''
    user_data = initialise_user_data

    token = user_data['user2']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': token,
    })

    assert requests.get(f'{url}/users/all', params={
        'token': token
    }).status_code == 400

'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Cyrus Wilkie

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
-> APP.route("/user/profile", methods=['GET']) return json.dumps({user})
-> APP.route("/auth/logout", methods=['POST']) return
   json.dumps({is_success})
-> APP.route("/user/profile/uploadphoto", methods=['POST']) return
   json.dumps({})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> reset
-> url
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> img_url returns an HTTP status other than 200.
    -> any of x_start, y_start, x_end, y_end are not within the 
       dimensions of the image at the URL
    -> Image uploaded is not a JPG
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_user_profile_uploadphoto_valid(url, initialise_user_data):
    '''
    Basic valid case of a user uploading a profile photo
    '''
    users = initialise_user_data

    profile = requests.get(f'{url}/user/profile', params={
        'token': users['user0']['token'],
        'u_id': users['user0']['u_id'],
    }).json()

    curr_img_url = profile['user']['profile_img_url']

    requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })

    profile = requests.get(f'{url}/user/profile', params={
        'token': users['user0']['token'],
        'u_id': users['user0']['u_id'],
    }).json()

    assert profile['user']['profile_img_url'] != curr_img_url

def test_user_profile_uploadphoto_invalid_http(url, initialise_user_data):
    '''
    Testing an invalid HTTP status return
    '''
    users = initialise_user_data

    assert requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://webcms3.cse.unsw.edu.au/gobbledegook.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 400

def test_user_profile_uploadphoto_large_dimensions(url, initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    assert requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 2000,
        'y_end': 2000,
    }).status_code == 400

def test_user_profile_uploadphoto_negative_dimensions(url, initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    assert requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg',
        'x_start': -10,
        'y_start': -10,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 400

def test_user_profile_uploadphoto_swapped_dimensions(url, initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    assert requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg',
        'x_start': 200,
        'y_start': 200,
        'x_end': 0,
        'y_end': 0,
    }).status_code == 400

def test_user_profile_uploadphoto_invalid_file(url, initialise_user_data):
    '''
    Testing a non jpg file
    '''
    users = initialise_user_data

    assert requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': users['user0']['token'],
        'img_url': 'https://pngimg.com/uploads/lightning/lightning_PNG52.png',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 400

def test_user_profile_uploadphoto_invalid_token(url, initialise_user_data):
    '''
    Testing with an invalid token
    '''
    users = initialise_user_data

    invalid_token = users['user0']['token']
    requests.post(f'{url}/auth/logout', json={
        'token': invalid_token,
    })

    requests.post(f'{url}/user/profile/uploadphoto', json={
        'token': invalid_token,
        'img_url': 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 400
'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 3
'''

import pytest
from auth import auth_logout
from user import user_profile, user_profile_uploadphoto
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
   return {}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
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

def test_user_profile_uploadphoto_valid(initialise_user_data):
    '''
    Basic valid case of a user uploading a profile photo
    '''
    users = initialise_user_data

    profile = user_profile(users['user0']['token'], users['user0']['u_id'])
    curr_img_url = profile['user']['profile_img_url']

    user_profile_uploadphoto(users['user0']['token'], 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg', 
                             0, 0, 200, 200)

    profile = user_profile(users['user0']['token'], users['user0']['u_id'])
    
    assert profile['user']['profile_img_url'] != curr_img_url

def test_user_profile_uploadphoto_invalid_http(initialise_user_data):
    '''
    Testing an invalid HTTP status return
    '''
    users = initialise_user_data

    with pytest.raises(InputError):
        user_profile_uploadphoto(users['user0']['token'], 'https://webcms3.cse.unsw.edu.au/gobbledegook.jpg', 0, 0, 200, 200)

def test_user_profile_uploadphoto_large_dimensions(initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    with pytest.raises(InputError):
        user_profile_uploadphoto(users['user0']['token'], 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg', 
                             0, 0, 2000, 2000)

def test_user_profile_uploadphoto_negative_dimensions(initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    with pytest.raises(InputError):
        user_profile_uploadphoto(users['user0']['token'], 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg', 
                             -10, -10, 200, 200)

def test_user_profile_uploadphoto_swapped_dimensions(initialise_user_data):
    '''
    Testing invalid (x, y) dimensions
    '''
    users = initialise_user_data

    with pytest.raises(InputError):
        user_profile_uploadphoto(users['user0']['token'], 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg', 
                             200, 200, 0, 0)

def test_user_profile_uploadphoto_invalid_file(initialise_user_data):
    '''
    Testing a non jpg file
    '''
    users = initialise_user_data

    with pytest.raises(InputError):
        user_profile_uploadphoto(users['user0']['token'], 'https://pngimg.com/uploads/lightning/lightning_PNG52.png', 
                             0, 0, 200, 200)

def test_user_profile_uploadphoto_invalid_token(initialise_user_data):
    '''
    Testing with an invalid token
    '''
    users = initialise_user_data

    invalid_token = users['user0']['token']
    auth_logout(users['user0']['token'])

    with pytest.raises(AccessError):
        user_profile_uploadphoto(invalid_token, 'https://webcms3.cse.unsw.edu.au/static/uploads/profilepic/z3418003/a17b8699d370d74996ef09e6044395d8330ddfe889ae1e364b5c8198b38d16a9/41250447_10214718102400449_1962109165832765440_n.jpg', 
                             0, 0, 200, 200)
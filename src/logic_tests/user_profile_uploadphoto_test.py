'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 2
'''

import pytest
from auth import auth_logout
from user import user_profile
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

    pass
    #users = initialise_user_data

    #user_profile_uploadphoto(users['user0']['token'], img_url, x_start, y_start, x_end, y_end)
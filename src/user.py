'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Cyrus Wilkie, Chitrakshi Gosain, Joseph Knox

Iteration 2 & 3
'''
import requests
import urllib.request
from PIL import Image
from error import InputError, AccessError
from helper import get_user_info, check_if_valid_email, \
check_string_length_and_whitespace, decode_encoded_token

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
-> user_profile_sethandle(token, handle_str) return {}
-> user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
   return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> u_id: integer
    -> user: dictionary containing u_id, email, name_first, name_last,
             handle_str
    -> name_first: string
    -> name_last: string
    -> email: string
    -> handle_str: string
    -> img_url: string
    -> x_start: int
    -> y_start: int
    -> x_end: int
    -> y_end: int
'''

'''
KEEP IN MIND:
-> allow multiple session log-ins,
   * for this make a data.data['valid_tokens'] dict in data.py, have
   tokens as key, and value as u_id this way we can keep track of
   multiple logins very easily, but don't do it now everyone will have to
   change implementation, do it after we are done merging all branches
   once, so if anything ever goes wrong we have A BACKUP. also, this
   ain't imp for itr 1 so don't stress. :)
'''

# CONSTANTS
MIN_CHAR_NAME_FIRST = 1
MAX_CHAR_NAME_FIRST = 50
MIN_CHAR_NAME_LAST = 1
MAX_CHAR_NAME_LAST = 50
MIN_CHAR_HANDLE_STR = 3
MAX_CHAR_HANDLE_STR = 20

def user_profile(token, u_id):
    '''
    DESCRIPTION:
    For a valid user, returns information about
    their user_id, email, first name, last name,
    and handle

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> u_id : user id of a user

    RETURN VALUES:
        -> user : information of user

    EXCEPTIONS:
    Error type: InputError
        -> user with u_id is not a valid_user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # Checking token validity
    user = get_user_info('token', token)
    if not user:
        raise AccessError(description='Token passed in is not a valid token')

    # Checking u_id validity and getting user data
    user = get_user_info('u_id', u_id)
    if not user:
        raise InputError(description='User with u_id is not a valid user')

    return {
        'user': {
        	'u_id': u_id,
        	'email': user['email'],
        	'name_first': user['name_first'],
        	'name_last': user['name_last'],
        	'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url'],
        },
    }

def user_profile_setname(token, name_first, name_last):
    '''
    DESCRIPTION:
    Given a token, replaces the authorised user's first and last name
    with the provided name_first and name_last respectively.

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> name_first : new first name of a user
        -> name_last : new last name of a user
    
    EXCEPTIONS:
    Error type: InputError
        -> name_first is not between 1 and 50 characters inclusively
            in length
        -> name_last is not between 1 and 50 characters inclusively
            in length
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # check if token is valid
    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    # check if name_first and name_last are of invalid length
    if not check_string_length_and_whitespace(MIN_CHAR_NAME_FIRST, \
                                             MAX_CHAR_NAME_FIRST, name_first):
        raise InputError(description='name_first is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    if not check_string_length_and_whitespace(MIN_CHAR_NAME_LAST, \
                                             MAX_CHAR_NAME_LAST, name_last):                                             
        raise InputError(description='name_last is not between 1 and 50 \
        characters inclusively in length or is a whitespace')

    user_info['name_first'] = name_first
    user_info['name_last'] = name_last

    return {
    }


def user_profile_setemail(token, email):
    '''
    DESCRIPTION:
    Updates the authorized user's email address

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> email : new email of a user

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email address is already being used by another user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # Checking for InputError(s) or AccessError:

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    if not check_if_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    if user_info['email'] == email:
        return {
        }

    if get_user_info('email', email):
        raise InputError(description='Email address is already being used by \
        another user')

    # Since there is no InputError or AccessError, hence proceeding
    # forward:

    user_info['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    DESCRIPTION:
    Updates the authorized user's handle (i.e. display name)

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> handle_str : new handle_str of a user

    EXCEPTIONS:
    Error type: InputError
        -> handle_str must be between 3 and 20 characters
        -> handle is already being used by another user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    # Checking for InputError(s) or AccessError:

    user_info = get_user_info('token', token)
    if not user_info:
        raise AccessError(description='Token passed in is not a valid token')

    if not check_string_length_and_whitespace(MIN_CHAR_HANDLE_STR, \
                                             MAX_CHAR_HANDLE_STR, handle_str):
        raise InputError(description='handle_str is not between 3 and 20 \
        characters inclusively in length or is a whitespace')

    if user_info['handle_str'] == handle_str:
        return {
        }

    if get_user_info('handle_str', handle_str):
        raise InputError(description='Handle is already being used by \
        another user')

    # Since there is no InputError or AccessError, hence proceeding
    # forward:

    user_info['handle_str'] = handle_str

    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    DESCRIPTION:
    Given a URL of an image on the internet, crops the image within
    bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the
    top left

    PARAMETERS:
        -> token : token of the authenticated user
        -> img_url : url of an image to be uploaded as profile photo
        -> x_start : start horizontal bound for image to be cropped from
        -> y_start : start vertical bound for image to be cropped from
        -> x_end : end horizontal bound for image to be cropped till
        -> y_end : end vertical bound for image to be cropped till
    
    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> img_url returns an HTTP status other than 200.
        -> any of x_start, y_start, x_end, y_end are not within the
           dimensions of the image at the URL.
        -> image uploaded is not a JPG
    '''

    # Checking token validity
    user = get_user_info('token', token)

    if not user:
        raise AccessError(description='Token passed in is not a valid token')

    # Checking file type
    if img_url.split('.')[-1] != 'jpg':
        raise InputError(description='Image uploaded is not a JPG')

    # Checking dimensions
    if x_start >= x_end or y_start >= y_end or x_start < 0 or y_start < 0:
        raise InputError(description='Invalid cropping coordinates')

    # Downloading image
    image = requests.get(img_url, stream=True)

    if image.status_code != 200:
        raise InputError(description='Specified URL returned an error status')

    img_file_name = f"{user['handle_str']}.jpg"
    urllib.request.urlretrieve(img_url, f"src/profile_img/{img_file_name}")

    # Opening image for editing
    photoImage = Image.open(f"src/profile_img/{img_file_name}")
    

    # Checking image size
    width, height = photoImage.size

    if x_start >= width or y_start >= height or x_end > width or y_end > height:
        raise InputError(description='Invalid cropping coordinates')

    # Cropping image
    croppedImage = photoImage.crop((x_start, y_start, x_end, y_end))
    croppedImage.save(f"src/profile_img/{img_file_name}")

    # Change the img url of user
    user['profile_img_url'] = f"profile_img/{img_file_name}"

    return {
    }
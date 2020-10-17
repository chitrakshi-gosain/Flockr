'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import pytest
import data
from other import clear
from error import InputError
from user import user_profile
from auth import auth_register

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> email entered is not a valid email
    -> email address is already being used by another user
    -> password entered is less than 6 characters long or more than 32
       characters long
    -> name_first is not between 1 and 50 characters inclusively in
       length
    -> name_last is not between 1 and 50 characters inclusively in
       length
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> check re registeration of a user
-> handle_str checks need to be done, will have to user user.py for it
'''

def test_trying_to_register_and_login_with_everything_valid():
    '''
    Tests that auth_register registers a new user successfully
    '''

    clear()
    auth_register('registerationtestvalidemailid0@gmail.com', '123Abc!0', \
                 'Valid', 'User0')

def test_invalid_email():
    '''
    Tests that auth_register raises an InputError when an invalid email
    is passed as one of the parameters
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestinvalidemailid0_gmail.com', \
                     '123Abc!!', 'Invalid', 'User0')

def test_existing_email_registration():
    '''
    Tests that auth_register raises an InputError when a user tries to
    register with an existing email-id in database registered with
    another user
    '''

    clear()
    auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', \
                 'Valid', 'User1')
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', \
                     'Valid', 'User1again')

def test_too_short_first_name():
    '''
    Tests that auth_register raises an InputError when a name_first less
    than 1 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid2@gmail.com', '123Abc!2', \
                     '', 'User2')

def test_too_long_first_name():
    '''
    Tests that auth_register raises an InputError when a name_first more
    than 50 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid3@gmail.com', '123Abc!3', \
                     'Valid' * 11, 'User3')

def test_too_short_last_name():
    '''
    Tests that auth_register raises an InputError when a name_last less
    than 1 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid4@gmail.com', '123Abc!4', \
                     '', 'User4')

def test_too_long_last_name():
    '''
    Tests that auth_register raises an InputError when a name_last more
    than 50 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid5@gmail.com', '123Abc!5', \
                     'Valid', 'User5' * 11)

def test_password_too_short_():
    '''
    Tests that auth_register raises an InputError when a password less
    than 6 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid6@gmail.com', '1Ab!6', \
                     'Valid', 'User6')

def test_password_too_long_():
    '''
    Tests that auth_register raises an InputError when a password more
    than 32 characters long
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid7@gmail.com', \
                     '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*7', 'Valid',\
                            'User7')

def test_insufficient_parameters():
    '''
    Tests that auth_login raises an InputError when less than expected
    parameters are passed
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid8@gmail.com', None, \
                     'Valid', 'User8')

def test_return_type():
    '''
    Tests that auth_register returns the expected datatype i.e.
    {u_id : int, token : str}
    '''

    clear()
    test_user_9 = auth_register('registerationtestvalidemailid9@gmail.com', \
                               '123Abc!9', 'Valid', 'User9')
    assert isinstance(test_user_9['u_id'], int)
    assert isinstance(test_user_9['token'], str)

def test_non_ascii_name_first():
    '''
    Tests that auth_register raises an InputError when a name_first is
    Non-ASCII
    '''

    clear()
    auth_register('registerationtestvalidemailid10@gmail.com', '123Abc!10', \
                 'Anaïs', 'User10')

def test_non_ascii_name_last():
    '''
    Tests that auth_register raises an InputError when a name_last is
    Non-ASCII
    '''

    clear()
    auth_register('registerationtestvalidemailid11@gmail.com', '123Abc!11', \
                 'Valid', 'सिंह')

def test_looking_for_negative_u_id():
    '''
    Tests that auth_register does not return a negative u_id
    '''

    clear()
    test_user_12 = auth_register('registerationtestvalidemailid12@gmail.com', \
                                '123Abc!12', 'Valid', 'User12')
    assert test_user_12['u_id'] >= 0

def test_non_ascii_password():
    '''
    Tests that auth_register raises an InputError when a password is
    Non-ASCII
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid13@gmail.com', \
                     'pass \n word', 'Valid', 'User13')

def test_whitespace_first_name():
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid14@gmail.com', \
                     '123Abc!14', '     ', 'User14')

def test_whitespace_last_name():
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    clear()
    with pytest.raises(InputError):
        auth_register('registerationtestvalidemailid15@gmail.com', \
                     '123Abc!15', '     ', 'User15')

def test_lowercase_handle():
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    '''

    clear()
    test_user_8 = auth_register('registerationtestvalidemailid8@gmail.com', \
                               '123Abc!8', 'Valid', 'User8')
    test_profile_8 = user_profile(test_user_8['token'], test_user_8['u_id'])
    assert test_profile_8['user']['handle_str'] == 'validuser8'

def test_unique_handle():
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. Each user has valid and
    different handle
    '''

    clear()
    test_user_9 = auth_register('registerationtestvalidemailid9@gmail.com', \
                               '123Abc!9', 'Valid', 'User9')
    test_profile_9 = user_profile(test_user_9['token'], test_user_9['u_id'])
    test_user_10 = auth_register('registerationtestvalidemailid10@gmail.com', \
                                '123Abc!10', 'Valid', 'User10')
    test_profile_10 = user_profile(test_user_10['token'], test_user_10['u_id'])
    assert test_profile_9['user']['handle_str'] != test_profile_10['user']['handle_str']

def test_too_long_handle():
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters
    '''

    clear()
    test_user_11 = auth_register('registerationtestvalidemailid11@gmail.com', \
                                '123Abc!11', 'Valid' * 2, 'User11' * 3)
    test_profile_11 = user_profile(test_user_11['token'], test_user_11['u_id'])
    assert test_profile_11['user']['handle_str'] == 'validvaliduser11user'

def test_handle_for_users_With_similar_first_last_names():
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. For a new user with
    similar name_first and name_last as one/more existing users there is
    some modification to new user's handle
    '''

    clear()
    test_user_12 = auth_register('registerationtestvalidemailid12@gmail.com', \
                                '123Abc!12', 'Valid', 'User12')
    test_user_13 = auth_register('registerationtestvalidemailid13@gmail.com', \
                                '123Abc!13', 'Valid', 'User13')
    test_user_14 = auth_register('registerationtestvalidemailid14@gmail.com', \
                                '123Abc!14', 'Valid', 'User13')
    test_user_15 = auth_register('registerationtestvalidemailid15@gmail.com', \
                                '123Abc!15', 'Valid', 'User12')
    for user in data.data['users']:
        if user['u_id'] == test_user_12['u_id']:
            user12_handle = user['handle_str']
        if user['u_id'] == test_user_13['u_id']:
            user13_handle = user['handle_str']
        if user['u_id'] == test_user_14['u_id']:
            user14_handle = user['handle_str']
        if user['u_id'] == test_user_15['u_id']:
            user15_handle = user['handle_str']

    assert user12_handle != user15_handle
    assert user13_handle != user14_handle
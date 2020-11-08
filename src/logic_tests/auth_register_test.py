'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 1
'''

import pytest
from error import InputError
from user import user_profile
from auth import auth_register

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> clear() return {}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> user_profile(token, u_id) return {user}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
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

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> check re registration of a user
-> handle_str checks need to be done, will have to user user.py for it
'''

def test_trying_to_register_with_everything_valid(reset):
    '''
    Tests that auth_register registers a new user successfully
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'user0_first', \
                 'user0_last')

def test_invalid_email(reset):
    '''
    Tests that auth_register raises an InputError when an invalid email
    is passed as one of the parameters
    '''

    with pytest.raises(InputError):
        auth_register('user0_email.com', 'user0_pass1!', 'user0_first', \
                     'user0_last')

def test_existing_email_registration(reset):
    '''
    Tests that auth_register raises an InputError when a user tries to
    register with an existing email-id in database registered with
    another user
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'user0_first', \
                 'user0_last')
    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', 'user0_first_again', \
                     'user0_last_again')

def test_too_short_first_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    less than 1 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', '', 'user0_last')

def test_too_long_first_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    more than 50 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', 'user0_first' * 5, \
                     'user0_last')

def test_too_short_last_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_last is
    less than 1 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', 'user0_first', '')

def test_too_long_last_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_last is
    more than 50 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', 'user0_first', \
                     'user0_last' * 6)

def test_password_too_short_(reset):
    '''
    Tests that auth_register raises an InputError when a password is
    less than 6 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0', 'user0_first', 'user0_last')

def test_password_too_long_(reset):
    '''
    Tests that auth_register raises an InputError when a password is
    more than 32 characters long
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                     !@#$%^&*7', 'user0_first', 'user0_last')

def test_return_type(reset):
    '''
    Tests that auth_register returns the expected datatype i.e.
    {u_id : int, token : str}
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_first', 'user0_last')
    assert isinstance(test_user_0['u_id'], int)
    assert isinstance(test_user_0['token'], str)

def test_non_ascii_name_first(reset):
    '''
    Tests that auth_register does not raise an InputError when a
    name_first is Non-ASCII
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'Anaïs', 'user0_last')

def test_non_ascii_name_last(reset):
    '''
    Tests that auth_register does not raise an InputError when a
    name_last is Non-ASCII
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'user0_first', 'सिंह')

def test_looking_for_negative_u_id(reset):
    '''
    Tests that auth_register does not return a negative u_id
    '''

    test_user_12 = auth_register('user0@email.com', 'user0_pass1!', \
                                'user0_first', 'user0_last')
    assert test_user_12['u_id'] >= 0

def test_non_ascii_password(reset):
    '''
    Tests that auth_register raises an InputError when a password is
    Non-ASCII
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0 \n pass1!', 'user0_first', \
                     'user0_last')

def test_whitespace_first_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', '    ', 'user0_last')

def test_whitespace_last_name(reset):
    '''
    Tests that auth_register raises an InputError when a name_first is
    completely whitespace
    '''

    with pytest.raises(InputError):
        auth_register('user0@email.com', 'user0_pass1!', 'user0_first', '    ')

def test_lowercase_handle(reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_FIRST', 'user0_LAST')
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_profile_0['user']['handle_str'] == 'user0_firstuser0_las'

def test_unique_handle(reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. Each user has valid and
    different handle
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_FIRST', 'user0_LAST')
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])

    test_user_1 = auth_register('user1@email.com', 'user1_pass1!', \
                               'user1_FIRST', 'user1_LAST')
    user_profile_1 = user_profile(test_user_1['token'], test_user_1['u_id'])

    assert user_profile_0['user']['handle_str'] != user_profile_1['user']\
        ['handle_str']

def test_too_long_handle_first_name(reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_FIRST' * 2, 'user0_LAST')
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_profile_0['user']['handle_str'] == 'user0_firstuser0_fir'

def test_too_long_handle_last_name(reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'u', 'user0_LAST' * 2)
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_profile_0['user']['handle_str'] == 'uuser0_lastuser0_las'

def test_handle_for_users_with_similar_first_last_names(reset):
    '''
    Tests that auth_register implements handle_str as per
    specifications, i.e. concatenates lowercase name_first and name_last
    and cuts it if greater than 20 characters. For a new user with
    similar name_first and name_last as one/more existing users there is
    some modification to new user's handle
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_first', 'user0_last')
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])

    test_user_1 = auth_register('user1@email.com', 'user1_pass1!', \
                               'user1_first', 'user1_last')
    user_profile_1 = user_profile(test_user_1['token'], test_user_1['u_id'])

    test_user_2 = auth_register('user2@email.com', 'user2_pass1!', \
                               'user0_first', 'user0_last')
    user_profile_2 = user_profile(test_user_2['token'], test_user_2['u_id'])

    test_user_3 = auth_register('user3@email.com', 'user3_pass1!', \
                               'user1_first', 'user1_last')
    user_profile_3 = user_profile(test_user_3['token'], test_user_3['u_id'])

    assert user_profile_0['user']['handle_str'] != user_profile_2['user']\
        ['handle_str']
    assert user_profile_1['user']['handle_str'] != user_profile_3['user']\
        ['handle_str']

def test_first_name_1_char(reset):
    '''
    Tests that auth_register accepts a name_first which is 1 character
    long
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'u', 'user0_last')

def test_first_name_50_chars(reset):
    '''
    Tests that auth_register accepts a name_first which is 50 characters
    long
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'u' * 50, 'user0_last')

def test_last_name_1_char(reset):
    '''
    Tests that auth_register accepts a name_last which is 1 character
    long
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'user0_first', 'u')

def test_last_name_50_chars(reset):
    '''
    Tests that auth_register accepts a name_last which is 50 characters
    long
    '''

    auth_register('user0@email.com', 'user0_pass1!', 'user0_first', 'u' * 50)

def test_password_6_chars(reset):
    '''
    Tests that auth_register accepts a password which is 6 characters
    long
    '''

    auth_register('user0@email.com', 'user0_', 'user0_first', 'user0_last')

def test_password_32_chars(reset):
    '''
    Tests that auth_register accepts a password which is 32 characters
    long
    '''

    auth_register('user0@email.com', 'user0_password1!' * 2, 'user0_first', \
                 'user0_last')

def test_details_registered_by_auth_register(reset):
    '''
    Tests that auth_register has stored all the general details of a
    user correctly
    '''

    test_user_0 = auth_register('user0@email.com', 'user0_pass1!', \
                               'user0_first', 'user0_last')
    user_profile_0 = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_profile_0 == {
        'user': {
            'u_id': test_user_0['u_id'],
            'email': 'user0@email.com',
            'name_first': 'user0_first',
            'name_last': 'user0_last',
            'handle_str': 'user0_firstuser0_las',
            'profile_img_url': '',
        }
    }

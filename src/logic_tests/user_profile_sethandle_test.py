'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import pytest
from error import InputError, AccessError
from user import user_profile, user_profile_sethandle

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> user_profile(token, u_id) return {user}
-> user_profile_sethandle(toke, handle_str) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
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

def test_return_type(initialise_user_data):
    '''
    Tests that user_profile_sethandle returns the expected datatype i.e.
    {}
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_newhandle = user_profile_sethandle(test_user_0['token'], \
                                       'my_new_handle')
    assert isinstance(test_user_0_newhandle, dict)
    assert not test_user_0_newhandle

def test_invalid_token(initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an AccessError when an
    invalid token is passed as one of the parameters
    '''

    with pytest.raises(AccessError):
        user_profile_sethandle('some_token', 'a_new_handle')

def test_too_short_handle_str(initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a
    handle entered by user for updatation is less than 3 characters
    long
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], 'me')

def test_too_long_handle_str(initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a
    handle entered by user for updatation is more than 20 characters
    long
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], 'me_' * 7)

def test_successful_handle_updatation(initialise_user_data):
    '''
    Tests that user_profile_sethandle updates handle of a user to an
    handle entered by user, if it does not exist in database i.e. it
    is not being used by any registered user at that instance
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_sethandle(test_user_0['token'], 'user_0_handle')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['handle_str'] == 'user_0_handle'

def test_handle_3_chars(initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    is 3 characters long
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_sethandle(test_user_0['token'], 'me_')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['handle_str'] == 'me_'

def test_handle_20_chars(initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    is 20 characters long
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_sethandle(test_user_0['token'], 'hi' * 10)
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['handle_str'] == 'hi' * 10

def test_non_ascii_handle(initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts a new handle by user which
    has Non-ASCII characters
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_sethandle(test_user_0['token'], 'âêîôû é àèù ëïü')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['handle_str'] == 'âêîôû é àèù ëïü'

def test_existing_handle(initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a user
    tries to update his handle to an existing handle in database
    registered with another user
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], 'user1_firstuser1_las')

def test_whitespace_handle(initialise_user_data):
    '''
    Tests that user_profile_sethandle raises an InputError when a handle
    entered by user for updatation is completely whitespace
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], '       ')

def test_no_change(initialise_user_data):
    '''
    Tests that user_profile_sethandle does not raise an InputError when
    a user tries to update his handle to an existing handle in
    database registered with himself
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_newhandle = user_profile_sethandle(test_user_0['token'], \
                                                  'user0_firstuser0_las')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])

    assert user_0_details['user']['handle_str'] == 'user0_firstuser0_las'
    assert isinstance(test_user_0_newhandle, dict)
    assert not test_user_0_newhandle

def test_only_unique_changes_accepted(initialise_user_data):
    '''
    Tests that user_profile_sethandle accepts to update a handle which
    previously belonged to another user and is now not a part of the
    database for a different user
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_sethandle(test_user_0['token'], 'user_0_handle')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['handle_str'] == 'user_0_handle'

    test_user_1 = initialise_user_data['user1']
    user_profile_sethandle(test_user_1['token'], 'user0_firstuser0_l')
    user_1_details = user_profile(test_user_1['token'], test_user_1['u_id'])
    assert user_1_details['user']['handle_str'] == 'user0_firstuser0_l'

    assert user_0_details['user']['handle_str'] != user_1_details['user']['handle_str']

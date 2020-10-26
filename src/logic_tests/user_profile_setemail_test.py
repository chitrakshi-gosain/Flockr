'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import pytest
from error import InputError, AccessError
from user import user_profile, user_profile_setemail

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> user_profile(token, u_id) return {user}
-> user_profile_setemail(token, email) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> email entered is not a valid email
    -> email address is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
'''

def test_return_type(initialise_user_data):
    '''
    Tests that user_profile_setemail returns the expected datatype i.e.
    {}
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_updatedemail = user_profile_setemail(test_user_0['token'], \
                                       'user0newemailid@email.com')
    assert isinstance(test_user_0_updatedemail, dict)
    assert not test_user_0_updatedemail

def test_invalid_token(initialise_user_data):
    '''
    Tests that user_profile_setemail raises an AccessError when an
    invalid token is passed as one of the parameters
    '''

    with pytest.raises(AccessError):
        user_profile_setemail('some_token', 'user0newemailid@email.com')

def test_invalid_email(initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when an
    invalid email is passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_0['token'], \
                             '.user0newemailid_email.com')

def test_existing_email(initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when a user
    tries to update his email-id to an existing email-id in database
    registered with another user
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_0['token'], 'user1@email.com')

def test_successful_email_updatation(initialise_user_data):
    '''
    Tests that user_profile_setemail updates email-id of a user to an
    email-id entered by user, if it does not exist in database i.e. it
    is not being used by any registered user at that instance
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_setemail(test_user_0['token'], 'user0newemailid@email.com')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['email'] == 'user0newemailid@email.com'

def test_only_unique_changes_accepted(initialise_user_data):
    '''
    Tests that user_profile_setemail accepts to update an email-id which
    previously belonged to another user and is now not a part of the
    database for a different user
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_setemail(test_user_0['token'], 'user0newemailid@email.com')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['email'] == 'user0newemailid@email.com'

    test_user_1 = initialise_user_data['user1']
    user_profile_setemail(test_user_1['token'], 'user0@email.com')
    user_1_details = user_profile(test_user_1['token'], test_user_1['u_id'])
    assert user_1_details['user']['email'] == 'user0@email.com'

    assert user_0_details['user']['email'] != user_1_details['user']['email']

def test_no_change(initialise_user_data):
    '''
    Tests that user_profile_setemail does not raise an InputError when a
    user tries to update his email-id to an existing email-id in
    database registered with himself
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_updatedemail = user_profile_setemail(test_user_0['token'], \
                                                       'user0@email.com')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])

    assert user_0_details['user']['email'] == 'user0@email.com'
    assert isinstance(test_user_0_updatedemail, dict)
    assert not test_user_0_updatedemail

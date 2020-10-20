'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import pytest
from other import clear
from error import InputError, AccessError
from user import user_profile, user_profile_setemail
from auth import auth_register

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
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> email entered is not a valid email
    -> email address is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
'''

@pytest.fixture
def reset():
    '''
    Resets the internal data of the application to it's initial state
    '''

    clear()

@pytest.fixture
def initialise_user_data():
    '''
    Sets up various user descriptive sample data for testing
    purposes and returns user data which is implementation dependent
    '''

    user0_details = auth_register('user0@email.com', 'user0_pass1!', \
                                 'user0_first', 'user0_last')
    user1_details = auth_register('user1@email.com', 'user1_pass1!', \
                                 'user1_first', 'user1_last')

    return {
        'user0': user0_details,
        'user1': user1_details
    }

def test_insufficient_parameters(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when less than
    expected parameters are passed
    '''

    with pytest.raises(InputError):
        user_profile_setemail(None, None)

def test_return_type(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail returns the expected datatype i.e.
    {}
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_updatedemail = user_profile_setemail(test_user_0['token'], \
                                       'mynewemail0@email.com')
    assert isinstance(test_user_0_updatedemail, dict)
    assert not test_user_0_updatedemail

def test_invalid_token(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an AccessError when an
    invalid token is passed as one of the parameters
    '''

    with pytest.raises(AccessError):
        user_profile_setemail('some_token', 'logintestvalidemailid@email.com')

def test_invalid_email(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when an
    invalid email is passed as one of the parameters
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_0['token'], \
                             'logintestinvalidemailid_email.com')

def test_existing_email(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail raises an InputError when a user
    tries to update his email-id to an existing email-id in database
    registered with another user
    '''

    test_user_0 = initialise_user_data['user0']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_0['token'], 'user1@email.com')

def test_successful_email_updatation(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail updates email-id of a user to an
    email-id entered by user, if it does not exist in database i.e. it
    is not being used by any registered user at that instance
    '''

    test_user_0 = initialise_user_data['user0']
    user_profile_setemail(test_user_0['token'], 'user0newemailid@email.com')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])
    assert user_0_details['user']['email'] == 'user0newemailid@email.com'

def test_only_unique_changes_accepted(reset, initialise_user_data):
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

def test_no_change(reset, initialise_user_data):
    '''
    Tests that user_profile_setemail does not raise an InputError when a
    user tries to update his email-id to an existing email-id in
    database registered with himself

    # assumption: user tries to change email to the one which he is using already
    # do not throw an error
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_updatedemail = user_profile_setemail(test_user_0['token'], \
                                                       'user0@email.com')
    user_0_details = user_profile(test_user_0['token'], test_user_0['u_id'])

    assert user_0_details['user']['email'] == 'user0@email.com'
    assert isinstance(test_user_0_updatedemail, dict)
    assert not test_user_0_updatedemail

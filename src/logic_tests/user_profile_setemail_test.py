'''
Created collaboratively by Wed15Team2 2020 T3
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
def initialise_user_data():
    '''
    Resets the internal data of the application to it's initial state
    and sets up various user sample data (descriptive and realistic) for
    testing purposes and returns user data which is implementation
    dependent.
    '''
    clear()

    user0_details = auth_register('user0@email.com', 'user0_pass1!', \
                                 'user0_first', 'user0_last')
    user1_details = auth_register('user1@email.com', 'user1_pass!', \
                                 'user1_first', 'user1_last')
    user2_details = auth_register('user2@email.com', 'user2_pass!', \
                                 'user2_first', 'user2_last')
    user3_details = auth_register('user3@email.com', 'user3_pass!', \
                                 'user3_first', 'user3_last')
    user4_details = auth_register('user4@email.com', 'user4_pass!', \
                                 'user4_first', 'user4_last')
    user5_details = auth_register('user5@email.com', 'user5_pass!', \
                                 'user5_first', 'user5_last')
    user6_details = auth_register('user6@email.com', 'user6_pass!', \
                                 'user6_first', 'user6_last')
    user7_details = auth_register('user7@email.com', 'user7_pass!', \
                                 'user7_first', 'user7_last')
    user8_details = auth_register('user8@email.com', 'user8_pass!', \
                                 'user8_first', 'user8_last')
    user9_details = auth_register('user9@email.com', 'user9_pass!', \
                                 'user9_first', 'user9_last')
    user10_details = auth_register('user10@email.com', 'user10_pass!', \
                                 'user10_first', 'user10_last')
    user11_details = auth_register('user11@email.com', 'user11_pass!', \
                                 'user11_first', 'user11_last')

    return {
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'user6': user6_details,
        'user7': user7_details,
        'user8': user8_details,
        'user9': user9_details,
        'user10': user10_details,       
        'user11': user11_details
    }

def test_insufficient_parameters():
    '''
    ADD DOCSTRING HERE
    '''

    clear()
    with pytest.raises(InputError):
        user_profile_setemail(None, None)

def test_return_type(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_updatedemail = user_profile_setemail(test_user_0['token'], \
                                       'mynewemail0@email.com')
    assert isinstance(test_user_0_updatedemail, dict)
    # checking if returned is empty, may or may not work this line is
    #  == True, but pythonic
    assert not test_user_0_updatedemail

def test_invalid_token():
    '''
    ADD DOCSTRING HERE
    '''

    with pytest.raises(AccessError):
        user_profile_setemail('some_token', 'logintestvalidemailid@email.com')

def test_invalid_email(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_1 = initialise_user_data['user1']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_1['token'], \
                             'logintestinvalidemailid_email.com')

def test_existing_email(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # not unique email
    '''

    test_user_2 = initialise_user_data['user2']
    with pytest.raises(InputError):
        user_profile_setemail(test_user_2['token'], 'user1@email.com')

def test_successful_email_updatation(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_2 = initialise_user_data['user2']
    user_profile_setemail(test_user_2['token'], 'user2newemailid@email.com')
    user_2_details = user_profile(test_user_2['token'], test_user_2['u_id'])
    assert user_2_details['user']['email'] == 'user2newemailid@email.com'

def test_only_unique_changes_accepted(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # register two users, then change emails of both, but unique and
    # everything should be successful
    '''

    test_user_3 = initialise_user_data['user3']
    user_profile_setemail(test_user_3['token'], 'user3newemailid@email.com')
    user_3_details = user_profile(test_user_3['token'], test_user_3['u_id'])
    assert user_3_details['user']['email'] == 'user3newemailid@email.com'

    test_user_4 = initialise_user_data['user4']
    user_profile_setemail(test_user_4['token'], 'user3@email.com')
    user_4_details = user_profile(test_user_4['token'], test_user_4['u_id'])
    assert user_4_details['user']['email'] == 'user3@email.com'

    assert user_3_details['user']['email'] != user_4_details['user']['email']

def test_no_change(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # user tries to change email to the one which he is using already
    # do not throw an error
    '''

    test_user_5 = initialise_user_data['user5']
    test_user_5_updatedemail = user_profile_setemail(test_user_5['token'], \
                                                       'user5@email.com')
    user_5_details = user_profile(test_user_5['token'], test_user_5['u_id'])

    assert user_5_details['user']['email'] == 'user5@email.com'
    assert isinstance(test_user_5_updatedemail, dict)
    assert not test_user_5_updatedemail

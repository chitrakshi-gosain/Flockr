'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import pytest
from other import clear
from error import InputError, AccessError
from user import user_profile, user_profile_sethandle
from auth import auth_register

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
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> handle_str must be between 3 and 20 characters
    -> handle is already being used by another user
Error type: AccessError
    -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
-> i have some assumptions testing in test, add them to assumptions.md
'''

# trying something new, using a fixture for users, hope it goes well
@pytest.fixture
def initialise_user_data():
    '''
    Resets the internal data of the application to it's initial state
    and sets up various descriptive user sample data for testing
    purposes and returns user data which is implementation
    dependent
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
        user_profile_sethandle(None, None)

def test_return_type(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_0 = initialise_user_data['user0']
    test_user_0_newhandle = user_profile_sethandle(test_user_0['token'], \
                                       'my_new_handle')
    assert isinstance(test_user_0_newhandle, dict)
    assert not test_user_0_newhandle

def test_invalid_token():
    '''
    ADD DOCSTRING HERE
    '''

    with pytest.raises(AccessError):
        user_profile_sethandle('some_token', 'a_new_handle')

def test_too_short_handle_str(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_1 = initialise_user_data['user1']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_1['token'], 'me')

def test_too_long_handle_str(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_2 = initialise_user_data['user2']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_2['token'], 'me_' * 7)

def test_successful_handle_updatation(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_3 = initialise_user_data['user3']
    user_profile_sethandle(test_user_3['token'], 'user_3_handle')
    user_3_details = user_profile(test_user_3['token'], test_user_3['u_id'])
    assert user_3_details['user']['handle_str'] == 'user_3_handle'

def test_handle_3_chars(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_4 = initialise_user_data['user4']
    user_profile_sethandle(test_user_4['token'], 'me_')
    user_4_details = user_profile(test_user_4['token'], test_user_4['u_id'])
    assert user_4_details['user']['handle_str'] == 'me_'

def test_handle_20_chars(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_5 = initialise_user_data['user5']
    user_profile_sethandle(test_user_5['token'], 'hi' * 10)
    user_5_details = user_profile(test_user_5['token'], test_user_5['u_id'])
    assert user_5_details['user']['handle_str'] == 'hi' * 10

def test_non_ascii_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that handles can have non ascii chars
    non ascii characters for jôhnsmïth
    '''

    test_user_6 = initialise_user_data['user6']
    user_profile_sethandle(test_user_6['token'], 'âêîôû é àèù ëïü')
    user_6_details = user_profile(test_user_6['token'], test_user_6['u_id'])
    assert user_6_details['user']['handle_str'] == 'âêîôû é àèù ëïü'

def test_existing_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_7 = initialise_user_data['user7']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_7['token'], 'user1_firstuser1_las')

def test_whitespace_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that only white space cant be valid handle
    '''

    test_user_8 = initialise_user_data['user8']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_8['token'], '       ')

def test_no_change(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''
    test_user_9 = initialise_user_data['user9']
    test_user_9_newhandle = user_profile_sethandle(test_user_9['token'], \
                                                  'user9_firstuser9_las')
    user_9_details = user_profile(test_user_9['token'], test_user_9['u_id'])

    assert user_9_details['user']['handle_str'] == 'user9_firstuser9_las'
    assert isinstance(test_user_9_newhandle, dict)
    assert not test_user_9_newhandle

def test_only_unique_changes_accepted(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # register two users, then change handles of both, but unique and
    # everything should be successful, basically change handle of first
    # one to something new then second user successfully is able to take
    # the handle which previous user had first
    '''

    test_user_10 = initialise_user_data['user10']
    user_profile_sethandle(test_user_10['token'], 'user_10_handle')
    user_10_details = user_profile(test_user_10['token'], test_user_10['u_id'])
    assert user_10_details['user']['handle_str'] == 'user_10_handle'

    test_user_11 = initialise_user_data['user11']
    user_profile_sethandle(test_user_11['token'], 'user10_firstuser10_l')
    user_11_details = user_profile(test_user_11['token'], test_user_11['u_id'])
    assert user_11_details['user']['handle_str'] == 'user10_firstuser10_l'

    assert user_10_details['user']['handle_str'] != user_11_details['user']['handle_str']

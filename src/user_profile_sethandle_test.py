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
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
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

    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John',\
                                'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', \
                                'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', \
                                'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', \
                                  'Ingrid', 'Cline')

    return {
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'user6': user6_details,
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details
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
                                       'mynewemail0@gmail.com')
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

    test_user_jane = initialise_user_data['jane']
    user_profile_sethandle(test_user_jane['token'], 'jane.smith')
    jane_details = user_profile(test_user_jane['token'], test_user_jane['u_id'])
    assert jane_details['handle_str'] == 'jane.smith'

def test_handle_3_chars(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_3 = initialise_user_data['user3']
    user_profile_sethandle(test_user_3['token'], 'me_')
    user_3_details = user_profile(test_user_3['token'], test_user_3['u_id'])
    assert user_3_details['handle_str'] == 'me_'

def test_handle_20_chars(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_4 = initialise_user_data['user4']
    user_profile_sethandle(test_user_4['token'], 'hi' * 10)
    user_4_details = user_profile(test_user_4['token'], test_user_4['u_id'])
    assert user_4_details['handle_str'] == 'hi' * 10

def test_non_ascii_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that handles can have non ascii chars
    non ascii characters for jôhnsmïth
    '''

    test_user_john = initialise_user_data['john']
    user_profile_sethandle(test_user_john['token'], 'jôhnsmïth')
    john_details = user_profile(test_user_john['token'], test_user_john['u_id'])
    assert john_details['handle_str'] == 'jôhnsmïth'

def test_existing_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_5 = initialise_user_data['user5']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_5['token'], 'user4_firstuser4_las')

def test_whitespace_handle(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # this is an assumption like names that only white space cant be valid handle
    '''

    test_user_6 = initialise_user_data['user6']
    with pytest.raises(InputError):
        user_profile_sethandle(test_user_6['token'], '       ')

def test_no_change(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    test_user_noah = initialise_user_data['noah']
    test_user_noah_newhandle = user_profile_sethandle(test_user_noah['token'],\
                                                      'noah_navarro@yahoo.com')
    noah_details = user_profile(test_user_noah['token'], test_user_noah['u_id'])

    assert noah_details['handle_str'] == 'noah_navarro@yahoo.com'
    assert isinstance(test_user_noah_newhandle, dict)
    assert not test_user_noah_newhandle

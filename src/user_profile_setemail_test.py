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
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
-> user_profile_sethandle(toke, handle_str) return {}
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

    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John',\
                                'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', \
                                'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', \
                                'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', \
                                  'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df',\
                                  'Donald', 'Richards')

    return {
        'user0': user0_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details,
        'donald': donald_details
    }

def test_insufficient_parameters():
    '''
    ADD DOCTSRING HERE
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
                                       'mynewemail0@gmail.com')
    assert isinstance(test_user_0_updatedemail, dict)
    # checking if returned is empty, may or may not work 3 this line is
    # dic_is_empty == True, but pythonic
    dict_is_empty = not test_user_0_updatedemail
    assert dict_is_empty

def test_invalid_token(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

def test_invalid_email(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''
    pass

def test_existing_email(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # not unique email
    '''
    pass

def test_successful_email_updatation(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''
    pass

def test_only_unique_changes_accepted(initialise_user_data):
    '''
    ADD DOCSTRING HERE
    # register two users, then change emails of both, but unique and
    # everything should be successful
    '''
    pass

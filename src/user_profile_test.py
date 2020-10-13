from auth import auth_register, auth_logout
from user import user_profile
from other import clear
from error import AccessError, InputError
import pytest

# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Cyrus Wilkie

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> intialise_user_data() return {users}
-> 
'''

def initialise_user_data():
    '''
    Sets up various user sample data for testing purposes
    '''

    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Descriptive test data
    owner_details = auth_register('owner@email.com', 'Owner_pass1!', 'owner_first', 'owner_last')
    user1_details = auth_register('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    user2_details = auth_register('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    user3_details = auth_register('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    user4_details = auth_register('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
    user5_details = auth_register('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qweRt1uiop!', 'John', 'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'm3yDate0fb!rth', 'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RP&ssWord1', 'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o7563O*', 'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjDf2g@h@@df', 'Donald', 'Richards')

    # Returns user data that is implementation dependent (id, token)
    return {
        'owner': owner_details,
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

def test_user_profile_valid_basic():
    pass
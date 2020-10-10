'''
Created collaboratively by Wed15Team2 2020 T3
Contributer - Chitrakshi Gosain

Iteration 2
'''

import pytest
from other import clear
from error import InputError
from user import user_profile, user_profile_setemail, user_profile_sethandle

# edit basic template to fit this file

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_sucess}
'''

'''
EXCEPTIONS
Error type: InputError
    -> insufficient parameters
    -> email entered is not a valid email
    -> email entered does not belong to a user
    -> password is not correct
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> allow multiple logins
-> do we keep track of passwords? if in case user enters old password,
   then??, ask Hayden if this needs to be done
'''

def test_insufficient_parameters():
    '''
    ADD DOCTSRING HERE
    '''

    clear()

def test_return_type():
    '''
    ADD DOCSTRING HERE
    '''

    clear()

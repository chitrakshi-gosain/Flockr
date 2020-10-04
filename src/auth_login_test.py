# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain

# Iteration 1

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_sucess}
'''

'''
EXCEPTIONS
Error type: InputError
-> email entered is not valid
-> email entered does not belong to a user, i.e. not registered
-> password is incorrect
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> allow multiple logins
-> do we keep track of passwords? if in case user enters old password, then??, 
   ask Hayden if this needs to be done
'''

import auth
import pytest
from other import clear
from error import InputError
from user import user_profile

def test_successful_login_with_everything_valid():
    '''
    Tests that auth_login logs the user in successfully
    '''

    clear()
    test_user_0 = auth.auth_register('logintestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    auth.auth_logout(test_user_0['token'])
    auth.auth_login('logintestvalidemailid0@gmail.com', '123Abc!0')
    
def test_invalid_email():
    '''
    Tests that auth_login raises an InputError when an invalid email-is passed 
    as one of the parameters
    '''

    clear()
    test_user_exclamatory = auth.auth_register('logintestinvalidemailid@gmail.com', '123Abc!!', 'Valid', 'User!')
    auth.auth_logout(test_user_exclamatory['token'])
    with pytest.raises(InputError):
        auth.auth_login('logintestinvalidemailid_gmail.com', '123Abc!!')

def test_unregistered_user():
    '''
    Tests that auth_login raises an InputError when an unregistered user tries
    to log-in
    '''

    clear()
    test_user_1 = auth.auth_register('logintestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    auth.auth_logout(test_user_1['token'])
    with pytest.raises(InputError):
        auth.auth_login('unregisteredemail1@gmail.com', '123Abc!!')

def test_wrong_password():
    '''
    Tests that auth_login raises an InputError when a wrong password is passed 
    as one of the parameters
    '''
    clear()
    test_user_2 = auth.auth_register('logintestvalidemailid2@gmail.com', '123Abc!2', 'Valid', 'User2')
    auth.auth_logout(test_user_2['token'])
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid2@gmail.com', 'cbA321!!')

def test_insufficient_parameters():
    '''
    Tests that auth_login raises an InputError when less than expected 
    parameters are passed
    '''

    clear()
    test_user_3 = auth.auth_register('logintestvalidemailid3@gmail.com', '123Abc!3', 'Valid', 'User3')
    auth.auth_logout(test_user_3['token'])
    with pytest.raises(InputError):
        auth.auth_login('logintestvalidemailid3@gmail.com', None)

def test_return_type():
    '''
    Tests that auth_login returns the expected datatype i.e. 
    {u_id : int, token : str}
    '''

    clear()
    test_user_4 = auth.auth_register('registerationtestvalidemailid4@gmail.com', '123Abc!4', 'Valid', 'User4')
    auth.auth_logout(test_user_4['token'])
    test_user_4_login_credentials = auth.auth_login('registerationtestvalidemailid4@gmail.com', '123Abc!4')

    assert isinstance(test_user_4_login_credentials, dict)
    assert isinstance(test_user_4_login_credentials['u_id'], int)
    assert isinstance(test_user_4_login_credentials['token'], str) 

def test_login_u_id():
    '''
    Tests that auth_register and auth_login return same values of token and  
    u_id, as there may be a slightest possibility that token or u_id of the user 
    might be played around with
    '''

    clear()
    test_user_5_register_credentials = auth.auth_register('registerationtestvalidemailid5@gmail.com', '123Abc!5', 'Valid', 'User5')
    test_user_5_login_credentials = auth.auth_login('registerationtestvalidemailid5@gmail.com', '123Abc!5')
    assert test_user_5_login_credentials['u_id'] == test_user_5_register_credentials['u_id']

def test_login_unique_token_and_u_id():
    '''
    Tests that auth_login returns a unique u_id and token for each user
    '''

    clear()
    test_user_6 = auth.auth_register('registerationtestvalidemailid6@gmail.com', '123Abc!6', 'Valid', 'User6')
    auth.auth_logout(test_user_6['token'])
    test_user_6_login_credentials = auth.auth_login('registerationtestvalidemailid6@gmail.com', '123Abc!6')
    test_user_7 = auth.auth_register('registerationtestvalidemailid7@gmail.com', '123Abc!7', 'Valid', 'User7')
    auth.auth_logout(test_user_7['token'])
    test_user_7_login_credentials = auth.auth_login('registerationtestvalidemailid7@gmail.com', '123Abc!7')

    assert test_user_6_login_credentials != test_user_7_login_credentials

    tokens = [test_user_6_login_credentials['token'], test_user_7_login_credentials['token']]
    assert len(set(tokens)) == len(tokens)

def test_multiple_logins():
    '''
    Tests that auth_login allows multiple logins
    '''

    clear()
    auth.auth_register('registerationtestvalidemailid8@gmail.com', '123Abc!8', 'Valid', 'User8')
    auth.auth_login('registerationtestvalidemailid8@gmail.com', '123Abc!8')
    auth.auth_login('registerationtestvalidemailid8@gmail.com', '123Abc!8')

def test_looking_for_negative_u_id():
    '''
    Tests that auth_login does not return a negative u_id for a user
    '''

    clear()
    auth.auth_register('registerationtestvalidemailid9@gmail.com', '123Abc!9', 'Valid', 'User9')
    test_user_9_login_credentials = auth.auth_login('registerationtestvalidemailid9@gmail.com', '123Abc!9')
    assert test_user_9_login_credentials['u_id'] >= 0
    
def test_non_ascii_password():
    '''
    Tests that auth_login does not accept a Non-ASCII password as one the 
    parameters passed to it
    '''
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid13@gmail.com', 'pass \n word', 'Valid', 'User13')
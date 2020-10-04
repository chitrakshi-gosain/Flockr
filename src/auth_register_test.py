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
-> email is already being used by another user
-> password is less than 6 characters
-> name_first is not between 1 and 50 characters
-> name_last is not between 1 and 50 characters
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> check re registeration of a user 
-> handle_str checks need to be done, will have to user user.py for it 
'''

import auth
import pytest
from other import clear
from error import InputError
from user import user_profile

def test_trying_to_register_and_login_with_everything_valid():
    clear()
    auth.auth_register('registerationtestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')

def test_invalid_email():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestinvalidemailid0_gmail.com', '123Abc!!', 'Invalid', 'User0')

def test_existing_email_registeration():
    clear()
    auth.auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1again')

def test_too_short_first_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid2@gmail.com', '123Abc!2', '', 'User2')

def test_too_long_first_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid3@gmail.com', '123Abc!3', 'Valid' * 11, 'User3')

def test_too_short_last_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid4@gmail.com', '123Abc!4', '', 'User4')

def test_too_long_last_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid5@gmail.com', '123Abc!5', 'Valid', 'User5' * 11)

def test_password_too_short_():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid6@gmail.com', '1Ab!6', 'Valid', 'User6')

def test_password_too_long_(): # assuming max length is 32 characters, discuss
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid7@gmail.com', '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*7', 'Valid', 'User7')

def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid8@gmail.com', None, 'Valid', 'User8')

def test_return_type(): 
    clear()
    test_user_9_registeration_credentials = auth.auth_register('registerationtestvalidemailid9@gmail.com', '123Abc!9', 'Valid', 'User9')
    assert isinstance(test_user_9_registeration_credentials['u_id'], int)
    assert isinstance(test_user_9_registeration_credentials['token'], str)  

def test_non_ascii_name_first():
    clear()
    auth.auth_register('registerationtestvalidemailid10@gmail.com', '123Abc!10', 'Anaïs', 'User10')

def test_non_ascii_name_last():
    clear()
    auth.auth_register('registerationtestvalidemailid11@gmail.com', '123Abc!11', 'Valid', 'सिंह')

def test_looking_for_negative_u_id():
    clear()
    test_user_12_registeration_credentials = auth.auth_register('registerationtestvalidemailid12@gmail.com', '123Abc!12', 'Valid', 'User12')
    assert test_user_12_registeration_credentials['u_id'] >= 0

def test_non_ascii_password():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid13@gmail.com', 'pass \n word', 'Valid', 'User13')

def test_whitespace_first_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid14@gmail.com', '123Abc!14', '     ', 'User14')

def test_whitespace_last_name():
    clear()
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid15@gmail.com', '123Abc!15', '     ', 'User15')

# NOT NEEDED ATM:

# def test_lowercase_handle(): 
#     clear()
#     # test_user_8 = auth.auth_register('registerationtestvalidemailid8@gmail.com', '123Abc!8', 'Valid', 'User8')
#     # test_user_profile_8 = user_profile(test_user_8['token'], test_user_8['u_id'])
#     # assert test_user_profile_8['handle_str'] == 'validuser8'
#     pass
    
# def test_unique_handle():
#     clear()
#     # test_user_9 = auth.auth_register('registerationtestvalidemailid9@gmail.com', '123Abc!9', 'Valid', 'User9')
#     # test_user_profile_9 = user_profile(test_user_9['token'], test_user_9['u_id'])
#     # test_user_10 = auth.auth_register('registerationtestvalidemailid10@gmail.com', '123Abc!10', 'Valid', 'User10')
#     # test_user_profile_10 = user_profile(test_user_10['token'], test_user_10['u_id'])
#     # assert test_user_profile_9['handle_str'] != test_user_profile_10['handle_str']
#     pass

# def test_too_long_handle():
#     clear()
#     # test_user_11 = auth.auth_register('registerationtestvalidemailid11@gmail.com', '123Abc!11', 'Valid' * 2, 'User11' * 3)
#     # test_user_profile_11 = user_profile(test_user_11['token'], test_user_11['u_id'])
#     # assert test_user_profile_11['handle_str'] == 'validvaliduser11user'
#     pass

# NOT NEEDED SINCE REMOVED THE PASSWORD PATTERN CHECK:
# def test_password_without_lowercase():
#     clear()
#     with pytest.raises(InputError):
#         auth.auth_register('registerationtestvalidemailid10@gmail.com', '123ABC!10', 'Valid', 'User10')

# def test_password_without_uppercase():
#     clear()
#     with pytest.raises(InputError):
#         auth.auth_register('registerationtestvalidemailid11@gmail.com', '123abc!11', 'Valid', 'User11')

# def test_password_without_digit():
#     clear()
#     with pytest.raises(InputError):
#         auth.auth_register('registerationtestvalidemailid12@gmail.com', 'Abc!twelve', 'Valid', 'User12')

# def test_password_without_allowed_special_symbols():
#     clear()
#     with pytest.raises(InputError):
#         auth.auth_register('registerationtestvalidemailid13@gmail.com', '123abc 13', 'Valid', 'User13')

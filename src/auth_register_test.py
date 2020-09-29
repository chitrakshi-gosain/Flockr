# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Chitrakshi Gosain
# Reviewer - Ahmet K

# Iteration 1
'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_USED_FOR_THE_TEST(PARAMETERS) return (RETURN_TYPE):
-> auth_register(email, password, name_first, name_last) return (u_id, token)
-> auth_login(email,password) return (u_id, token)
'''

'''
EXCEPTIONS
Error type: InputError
-> email entered is not valid
-> email is already being used by another user
-> password is less than 6 characters
-> name_first is not between 1 and 50 characters
-> name_last is not between 1 and 50 characters
# for name check make a check_length function and send parameters to it during test
'''

'''
KEEP IN MIND:
-> user can be registered/non-registered, hence check
-> user can be already logged-in and trying to re-log-in, this has two 
   possibilties:
        *log-in to self account again
        *log-in to someone else's account
   however, in both cases user should be asked to logout first and then try
-> how to deal with re registeration of a user 
-> handle_str checks need to be done, will have to user use.py for it 
'''

import auth
import pytest
from error import InputError
from user import user_profile

def test_trying_to_register_and_login_with_everything_valid():
    auth.auth_register('registerationtestvalidemailid0@gmail.com', '123Abc!0', 'Valid', 'User0')
    auth.auth_login('registerationtestvalidemailid0@gmail.com', '123Abc!0')

def test_invalid_email():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestinvalidemailid0_gmail.com', '123Abc!!', 'Invalid', 'User0')

def test_existing_email_registeration():
    auth.auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1')
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid1@gmail.com', '123Abc!1', 'Valid', 'User1again')

def test_too_short_first_name():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid2@gmail.com', '123Abc!2', '', 'User2')
    
def test_too_short_last_name():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid3@gmail.com', '123Abc!3', '', 'User3')

def test_too_long_first_name():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid4@gmail.com', '123Abc!4', 'Valid' * 11, 'User4')

def test_too_long_last_name():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid5@gmail.com', '123Abc!5', 'Valid', 'User5' * 11)

def test_too_short_password():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid6@gmail.com', '12A!6', 'Valid', 'User6')

def test_too_long_password(): # assuming max length is 32 characters, discuss
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid7@gmail.com', '1234567890ABCDEFGHIJ!@#$%^&*()_+7', 'Valid', 'User7')

def test_lowercase_handle(): 
    test_user_8 = auth.auth_register('registerationtestvalidemailid8@gmail.com', '123Abc!8', 'Valid', 'User8')
    test_user_profile_8 = user.user_profile(test_user_8['token'], test_user_8['u_id'])
    assert test_user_profile_8['handle_str'] == 'validuser8'
    pass

def test_unique_handle():
    test_user_9 = auth.auth_register('registerationtestvalidemailid9@gmail.com', '123Abc!9', 'Valid', 'User9')
    test_user_profile_9 = user.user_profile(test_user_9['token'], test_user_9['u_id'])
    test_user_10 = auth.auth_register('registerationtestvalidemailid10@gmail.com', '123Abc!10', 'Valid', 'User10')
    test_user_profile_10 = user.user_profile(test_user_10['token'], test_user_10['u_id'])
    assert test_user_profile_9['handle_str'] != test_user_profile_10['handle_str']
    pass

def test_too_long_handle():
    test_user_11 = auth.auth_register('registerationtestvalidemailid11@gmail.com', '123Abc!11', 'Valid' * 2, 'User11' * 3)
    test_user_profile_11 = user.user_profile(test_user_11['token'], test_user_11['u_id'])
    assert test_user_profile_11['handle_str'] == 'validvaliduser11user'
    pass

def test_insufficient_parameters():
    with pytest.raises(InputError):
        auth.auth_register('registerationtestvalidemailid7@gmail.com', None, 'Valid', 'User7')
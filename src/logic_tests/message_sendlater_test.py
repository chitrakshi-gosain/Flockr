'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 3
'''

import pytest
from auth import auth_logout
from user import user_profile, user_profile_uploadphoto
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> message_sendlater(token, channel_id, message, time_sent) return
   {messsage_id}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> Channel ID is not a valid channel
    -> Message is more than 1000 characters
    -> Time sent is a time in the past
Error type: AccessError
    -> token passed in is not a valid token
    -> The authorised user has not joined the channel they are trying
       to post to
'''
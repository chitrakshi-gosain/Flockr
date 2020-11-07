'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Cyrus Wilkie

Iteration 3
'''

import pytest
from datetime import timezone, datetime
from auth import auth_logout
from message import message_sendlater
from error import AccessError, InputError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> message_sendlater(token, channel_id, message, time_sent) return
   {message_id}
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_logout(token) return {is_success}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
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

def test_message_sendlater_valid(initialise_user_data, initialise_channel_data):
    '''
    Testing a basic valid case
    '''
    users = initialise_user_data
    channels = initialise_channel_data

    curr_time = datetime.now()
    time_sent = curr_time + datetime(0, 0, 0, 0, 1, 0, 0)

    message_id = message_sendlater(users['user0']['token'], channels['user0_publ']['channel_id'], 
        'Hello World!', time_sent)

    assert isInstance(message_id['message_id'], int)


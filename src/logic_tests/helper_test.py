'''
Created collaboratively by Wed15Team2 2020 T3
Contributors - Jordan Hunyh, Chitrakshi Gosain, Cyrus Wilkie,
               Ahmet Karatas, Joseph Knox

Iteration 2
'''

import pytest
from channel import channel_join, channel_messages
from helper import encrypt_password_with_hash, generate_encoded_token, \
    decode_encoded_token, get_channel_info, get_message_info, get_user_info, \
        is_channel_owner, is_user_authorised, is_user_in_channel, \
            check_if_valid_email, check_if_valid_password, \
                check_string_length_and_whitespace, invalidating_token, \
                post_message_to_channel
import data
from error import InputError, AccessError
from datetime import datetime, timezone

'''
****************************BASIC TEMPLATE******************************
'''

'''
This file contains test for all the helper functions used throughout the 
implementation of interface
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, firstname, lastname)
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
'''

def test_check_if_valid_email(reset):
    '''
    Given the email of the user to be registered checks if it is a
    valid email using a regex
    '''
    # Invalid Cases
    assert not check_if_valid_email('blatantlywrong')
    assert not check_if_valid_email('vaguelytrying@')
    assert not check_if_valid_email('abitcloser@gmail')
    assert not check_if_valid_email('@ozemail.com.au')
    assert not check_if_valid_email('')

    # Valid Cases
    assert check_if_valid_email('ingridcline@gmail.com')
    assert check_if_valid_email('myemail@email.com')
    assert check_if_valid_email('hi@hello.com')


def test_check_if_valid_password(reset):
    '''
    Tests the password of the user to be registered checks it's length
    is in valid range and if it has printable ASCII characters only
    '''

    # Invalid Cases
    assert not check_if_valid_password('')
    assert not check_if_valid_password('hello')
    assert not check_if_valid_password('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c\
        1fa7425e73043362938b9824helloworld')
    assert not check_if_valid_password('hello\nworld')

    # Valid Cases
    assert check_if_valid_password('mysecuredateofbirth')
    assert check_if_valid_password('1234567890') 
    assert check_if_valid_password('another valid pasword') 
    assert check_if_valid_password('*&%&%*)^*#$') 

def test_check_string_length_and_whitespace(reset, initialise_data):
    '''
    Tests name_first(1-50 char limit), name_last(1-50 char limit) and
    handle_str(3-20 char limit), all char limits are inclusive
    '''

    #Out of length range
    assert not check_string_length_and_whitespace(6,32,'123')
    assert not check_string_length_and_whitespace(6,32,'0123456789012345678901234567890123')
    #Edge
    assert check_string_length_and_whitespace(6,32,'123456')
    assert check_string_length_and_whitespace(6,32,'01234567890123456789012345678901')
    #Spaces
    assert not check_string_length_and_whitespace(5,20,'        ')


def test_get_channel_info(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    assert not get_channel_info(-1)
    assert get_channel_info(0) == data.data['channels'][0]
    assert get_channel_info(1) == data.data['channels'][1]

def test_is_user_authorised(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    user0 = get_user_info('u_id', 0)
    token0 = user0['token']
    user1 = get_user_info('u_id', 1)
    token1 = user1['token']

    assert is_user_authorised(generate_encoded_token(token0), 0)
    assert is_user_authorised(generate_encoded_token(token0), 1)
    assert is_user_authorised(generate_encoded_token(token1), 1)
    assert not is_user_authorised(generate_encoded_token(token1), 0)


def test_is_channel_owner(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    assert is_channel_owner(0, 0)
    assert not is_channel_owner(0, 1)
    assert is_channel_owner(1, 1)
    assert not is_channel_owner(1, 0)

def test_get_user_info(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    assert not get_user_info('u_id', -1)
    assert not get_user_info('token', ' ')
    assert not get_user_info('email', ' ')

    assert get_user_info('u_id', 0) == data.data['users'][0]
    assert get_user_info('token', generate_encoded_token('0')) == \
        data.data['users'][0]
    assert get_user_info('email', 'blah1@domain') == data.data['users'][1]

def test_is_user_in_channel(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    assert is_user_in_channel(0, 0)
    assert is_user_in_channel(0, 1)
    assert is_user_in_channel(1, 0)
    assert is_user_in_channel(1, 1)

def test_get_message_info(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    assert get_message_info(0) == {
        'message_id': 0,
        'u_id': 0,
        'message': 'messagecontents0',
        'timecreated': 'datetime(YYYY, MM, DD, HH, MM)'
    }
    assert get_message_info(1) == {
        'message_id': 1,
        'u_id': 0,
        'message': 'messagecontents1',
        'timecreated': 'datetime(YYYY, MM, DD, HH, MM)'
    }

def test_encrypt_same_password_with_hash(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    password = 'user0_pass1!'
    pass_hash = encrypt_password_with_hash(password)
    assert pass_hash == encrypt_password_with_hash(password)

def test_encrypt_different_password_with_hash(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    password1 = 'user0_pass1'
    password2 = 'user1_pass1'
    pass_hash1 = encrypt_password_with_hash(password1)
    assert pass_hash1 != encrypt_password_with_hash(password2)

def test_generate_encoded_token(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    u_id0 = 0
    token0 = generate_encoded_token(u_id0)

    u_id1 = 1
    token1 = generate_encoded_token(u_id1)

    assert token0 != str(u_id0)
    assert token1 != str(u_id1)
    #check if stored in data
    assert {token0 : u_id0} in data.data['valid_tokens']
    assert {token1 : u_id1} in data.data['valid_tokens']

    with pytest.raises(AccessError):
        invalidating_token(decode_encoded_token('some_token'))


def test_decode_encoded_token(reset, initialise_data):
    '''
    ADD DOCSTRING HERE
    '''

    encoded_token = generate_encoded_token('234')
    decoded_token = decode_encoded_token(encoded_token)
    assert encoded_token != '234'
    assert encoded_token != decoded_token
    assert decoded_token == '234'

    with pytest.raises(AccessError):
        invalidating_token(decode_encoded_token('some_token'))

def test_invalidating_token(reset, initialise_user_data):
    '''
    ADD DOCSTRING HERE
    '''

    user0_token = initialise_user_data['user0']['token']
    decoded_token = decode_encoded_token(user0_token)
    logout_status = invalidating_token(decoded_token)
    assert logout_status

    assert not invalidating_token('    ')
    assert not invalidating_token(generate_encoded_token('1234'))

    with pytest.raises(InputError):
     assert not invalidating_token(generate_encoded_token('some_token'))

def test_post_message_to_channel(reset, initialise_user_data, initialise_channel_data):
    '''
    Posts a message already present in data['messages'] to the relevant channel
    '''

    users = initialise_user_data
    channels = initialise_channel_data

    message = 'Hello World!'
    curr_time = datetime.now()
    curr_time = curr_time.replace(tzinfo=timezone.utc).timestamp()

    message_dict = {
        'message_id': 1,
        'u_id': users['user0']['u_id'],
        'message': message,
        'time_created': curr_time,
    }

    channel_join(users['user0']['token'], channels['user0_publ']['channel_id'])
    post_message_to_channel(message_dict, channels['user0_publ']['channel_id'])
    message_list = channel_messages(users['user0']['token'], channels['user0_publ']['channel_id'], 0)

    assert message_list['messages'][0] == message_dict

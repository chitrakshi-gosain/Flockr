# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 2

import pytest
import auth
import helper
from channel import channel_join
from channels import channels_create
from message import message_send, message_edit
from error import AccessError
from other import clear

'''
*********************************BASIC TEMPLATE*********************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return {u_id, token}
-> channel_join(token, channel_id) return {}
-> channels_create(token, name, is_public) return {channel_id}
-> message_send(token, channel_id, message) return {message_id}
-> message_edit(token, message_id, message) return {}
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
    -> authorised user is not an admin of the flockr or owner of the channel
    -> Message with message_id was not sent by the authorised user making this request
'''

def test_message_edit_noerrors():
    '''
    basic test with no edge case or errors raised
    '''
    clear()

    user_details = auth.auth_register("user@email.com", "user_pass", "user_first", "user_last")
    token = user_details['token']

    channel_dict = channels_create(token, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    message_edit(token, message_id, second_message)

    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == second_message

def test_message_edit_emptystring():
    '''
    test that message_edit deletes the message
    if provided with an empty string
    '''
    clear()

    user_details = auth.auth_register("user@email.com", "user_pass", "user_first", "user_last")
    token = user_details['token']

    channel_dict = channels_create(token, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = ""

    message_edit(token, message_id, second_message)

    # get_message_from_id returns False if message does not exist
    # therefore check that message has been deleted
    message_dict = helper.get_message_info(message_id)
    assert not message_dict

def test_message_edit_notsender():
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''
    clear()

    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    token1 = user1_details['token']

    # user0 creates channel, user1 joins it
    channel_dict = channels_create(token0, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]
    channel_join(token1, channel_id)

    first_message = "This is the original message."

    message_info = message_send(token0, channel_id, first_message)
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    with pytest.raises(AccessError):
        message_edit(token1, message_id, second_message)

def test_message_edit_notauth():
    '''
    test that message_edit raises AccessError
    if token is not authorised
    i.e. user is not admin of the flockr or owner of the channel message is in
    '''
    clear()

    user_details = auth.auth_register("user@email.com", "user_pass", "user_first", "user_last")
    token = user_details['token']

    channel_dict = channels_create(token, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]
    message_dict = helper.get_message_info(message_id)
    assert message_dict['message'] == first_message

    second_message = "This is the edited message."

    # assume " " is not a valid token
    token = " "

    with pytest.raises(AccessError):
        message_edit(token, message_id, second_message)

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

def test_message_edit_secondmessage():
    '''
    edits the second sent message, not the first
    '''
    clear()

    user_details = auth.auth_register("user@email.com", "user_pass", "user_first", "user_last")
    token = user_details['token']

    channel_dict = channels_create(token, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]

    first_message0 = "This is the first original message."
    first_message1 = "This is the second original message."

    message_info0 = message_send(token, channel_id, first_message0)
    message_id0 = message_info0["message_id"]
    message_dict0 = helper.get_message_info(message_id0)
    assert message_dict0['message'] == first_message0

    message_info1 = message_send(token, channel_id, first_message1)
    message_id1 = message_info1["message_id"]
    message_dict1 = helper.get_message_info(message_id1)
    assert message_dict1['message'] == first_message1

    second_message1 = "This is the second edited message."

    message_edit(token, message_id1, second_message1)

    message_dict1 = helper.get_message_info(message_id1)
    assert message_dict1['message'] == second_message1

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

def test_message_edit_notsenderorauth():
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    and user is not admin of the flockr or owner of the channel message is in
    '''
    clear()

    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    # user1 is not admin of the flockr
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

# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Joseph Knox

# Iteration 2

import pytest
import auth
from channel import channel_join
from channels import channels_create, channels_listall
from message import message_send, message_edit
from error import AccessError
from other import clear, search

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

    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            assert message['message'] == first_message
            break

    second_message = "This is the edited message."

    message_edit(token, message_id, second_message)

    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            assert message['message'] == second_message
            break

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
    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id0:
            assert message['message'] == first_message0
            break

    message_info1 = message_send(token, channel_id, first_message1)
    message_id1 = message_info1["message_id"]

    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id1:
            assert message['message'] == first_message1
            break
    
    second_message1 = "This is the second edited message."

    message_edit(token, message_id1, second_message1)

    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id1:
            assert message['message'] == second_message1
            break

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

    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            assert message['message'] == first_message
            break

    second_message = ""

    message_edit(token, message_id, second_message)

    # assert that message does not exist
    message_list = search(token, '')['messages']
    assert message_id not in [message['message_id'] for message in message_list]

def test_message_edit_notsender():
    '''
    test that message_edit raises AccessError
    if user (based on token) is not the sender of message with message ID message_id
    '''
    clear()

    # user0 with u_id0 and token0 is the first to register, thus also admin of the flockr
    user0_details = auth.auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    token0 = user0_details['token']

    # user1 with u_id1 and token1 is not admin
    user1_details = auth.auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    token1 = user1_details['token']

    # token0 creates channel, therefore user0 is member and owner of that channel
    channel_info = channels_create(token0, "ch_name0", True)
    channel_id = channel_info['channel_id']

    # token1 joins channel, therefore is a member but not an owner
    channel_join(token1, channel_id)

    first_message = "This is the original message."

    message_info = message_send(token0, channel_id, first_message)
    message_id = message_info["message_id"]

    # 'search' with empty query string returns list of all messages
    message_list = search(token0, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            assert message['message'] == first_message
            break

    second_message = "This is the edited message."

    # user1 did not send the original message, so token1 should fail
    with pytest.raises(AccessError):
        message_edit(token1, message_id, second_message)

def test_message_edit_notauth():
    '''
    test that message_edit raises AccessError
    if token is invalid
    '''
    clear()

    user_details = auth.auth_register("user@email.com", "user_pass", "user_first", "user_last")
    token = user_details['token']

    channel_dict = channels_create(token, "A Channel Name", True)
    channel_id = channel_dict["channel_id"]

    first_message = "This is the original message."

    message_info = message_send(token, channel_id, first_message)
    message_id = message_info["message_id"]

    # 'search' with empty query string returns list of all messages
    message_list = search(token, '')['messages']
    for message in message_list:
        if message['message_id'] == message_id:
            assert message['message'] == first_message
            break

    second_message = "This is the edited message."

    # assume " " is not a valid token
    token = " "

    with pytest.raises(AccessError):
        message_edit(token, message_id, second_message)

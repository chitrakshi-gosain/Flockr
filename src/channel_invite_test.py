import channel
from data import data

import pytest
from error import InputError
from error import AccessError

'''
Tests for channel_invite()

Parameters:(token, channel_id, u_id)

Return type: {}

Exceptions: InputError ->
                channel_id does not reffer to a valid channel that the
                    authorised user is part of
                u_id does not refer to valid user
            AccessError ->
                the authorised user is not already a member of the channel

Description: Invites a user (with user id u_id) to join a channel with ID
             channel_id. Once invited the user is added to the channel
             immediately

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2


'''
Current assumptions:
    1. User cannot be invited if they are already in the channel
'''

'''
Test ideas: [description] - [pass / fail / error]
    1. channel_id is invalid - InputError
    2. invalid user is added - InputError
    3. authorised user is not in channel - AccessError
    4. user is already in channel - fail
    5. valid channel_id and users - pass
'''

def test_channel_invite_invalid_channel():
    pass

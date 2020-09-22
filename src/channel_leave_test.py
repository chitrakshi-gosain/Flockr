import pytest
from error import InputError
from error import AccessError

'''
Tests for channel_leave()

Parameters:(token, channel_id)

Return type: {}

Exceptions: InputError ->
                Channel ID is not a valid channel
            AccessError ->
                Authorised user is not a member of channel with channel_id

Description: Given a channel ID, the user removed as a member of this channel

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2


'''
Current assumptions:
    1. Users are valid when/if they try leave the channel
    2. Should directly modify data if it works (and we check if data has changed to verify)
    3. Users cannot leave a channel if they are not in the channel

'''

'''
Test ideas: [description] - [pass / fail / error]
    1. Channel does not exist - InputError
    2. User is not part of the channel when they try leave - AccessError
    3. channel_id is valid and user is in channel - pass
'''

def test_channel_leave():
    pass

import pytest
from error import InputError
from error import AccessError

'''
Tests for channel_join()

Interface:
Parameters:(token, channel_id)

Return type: {}

Exceptions: InputError ->
                Channel ID is not a valid channel
            AccessError ->
                channel_id refers to a channel that is private
                    (when the authorised user is not an admin)

Description: Given a channel_id of a channel that the authorised user can join,
             adds them to that channel

'''

# Jordan Huynh (z5169771)
# Wed15 Grape 2


'''
Current assumptions:
    1. User cannot join if they are already in the channel
    2. Users are valid when/if they try join the channel
    3. Should directly modify data if it works (and we check if data has changed to verify)

'''

'''
Test ideas: [description] - [pass / fail / error]
    1. channel_id does not exist - InputError
    2. channel is private (and user is not admin) - AccessError
    3. channel is private (and user is admin) - pass
    4. user is already in channel - fail
    5. valid public channel_id and user is not in channel - pass
'''

def test_channel_join():
    pass

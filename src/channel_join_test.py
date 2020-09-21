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
'''

def test_channel_join():
    #todo

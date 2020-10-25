from other import clear
from channel import channel_invite, channel_join, channel_details
from auth import auth_register
from channels import channels_create

import pytest
from error import InputError, AccessError

#note: the following functions should be implemented:
    #auth_register, channels_create, channel_join, channel_details

def test_check_empty(initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    details = channel_details(token, channel_id)

    assert details # not empty

    clear()
    with pytest.raises(AccessError): #expect AccessError as all data has been cleared
        assert channel_details(token, channel_id)

#Should we add more tests or is this fine?

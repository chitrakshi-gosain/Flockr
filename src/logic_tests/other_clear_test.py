from other import clear
from channel import channel_invite, channel_join, channel_details
from auth import auth_register
from channels import channels_create

import pytest
from error import InputError, AccessError

#note: the following functions should be implemented:
    #auth_register, channels_create, channel_join, channel_details

def initialise_data():
    #create users
    #The first user to sign up is global owner
    admin_details = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    user0_details = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    user1_details = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    #create channels
    channel_publ_details = channels_create(admin_details['token'], "publ0", True)
    channel_priv_details = channels_create(admin_details['token'], "priv0", False)

    return ({ # users
        'admin' : admin_details,
        'user0' : user0_details,
        'user1' : user1_details,
    },
    { # channels
        'publ' : channel_publ_details,
        'priv' : channel_priv_details,
    })

def test_check_empty():
    clear() #meta?

    users, channels = initialise_data()
    details = channel_details(users['admin']['token'], channels['publ']['channel_id'])

    assert details # not empty

    clear()
    with pytest.raises(AccessError): #expect AccessError as all data has been cleared
        assert channel_details(users['admin']['token'], channels['publ']['channel_id'])

#Should we add more tests or is this fine?

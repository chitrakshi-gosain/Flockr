from other import clear
from channel import channel_invite, channel_join, channel_details
from auth import auth_register
import channels

import pytest
from error import InputError, AccessError

#note: the following functions should be implemented:
    #auth_register, channels_create, channel_join, channel_details

def initialise_data():
    #create users
    #The first user to sign up is global owner
    (admin_id, admin_token) = auth_register("admin@email.com", "admin_pass", "admin_first", "admin_last")
    (user0_id, user0_token) = auth_register("user0@email.com", "user0_pass", "user0_first", "user0_last")
    (user1_id, user1_token) = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
    #create channels
    channel_publ_id = channels_create(admin_token, "publ0", True)
    channel_priv_id = channels_create(admin_token, "priv0", False)

    channel_join(admin_token, channel_publ_id)
    channel_join(user0_token, channel_publ_id)
    channel_join(admin_token, channel_priv_id)

    return { # users
        'admin' : {'u_id': admin_id, 'token': admin_token, 'is_admin': True},
        'user0' : {'u_id': user0_id, 'token': user0_token, 'is_admin': False},
        'user1' : {'u_id': user1_id, 'token': user1_token, 'is_admin': False},
    },
    { # channels
        'publ' : {'ch_id': channel_publ_id},
        'priv' : {'ch_id': channel_priv_id},
    }

def check_empty():
    clear() #meta?

    users, channels = initialise_data()
    name, owners, members = channel_details(user['admin']['token'], channels['publ']['ch_id'])

    clear()
    with pytest.raises(AccessError) as e: #expect AccessError as all data has been cleared
        assert channel_details(user['admin']['token'], channels['publ']['ch_id'])

#Should we add more tests or is this fine?

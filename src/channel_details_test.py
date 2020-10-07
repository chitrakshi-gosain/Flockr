# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Ahmet Karatas

# Iteration 1

from auth import auth_register
from channel import channel_details, channel_join
from channels import channels_create
from other import clear
from error import InputError
from error import AccessError
import pytest


def test_insufficient_parameters():
    clear()
    with pytest.raises(InputError):
        channel_details(None, None)

def test_user_not_authorised():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1
    with pytest.raises(AccessError):
        channel_details(user1_credentials['token'], channel1_id['channel_id'])


def test_channel_id_not_valid():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner

    invalid_channel_id = -1 
    with pytest.raises(InputError):
        channel_details(owner_credentials['token'], invalid_channel_id)


def test_token_invalid():
    clear()

    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)
    with pytest.raises(AccessError):
        channel_details('incorrect_user1_token', channel1_id['channel_id'])

def test_return_type():
    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel

    # Invite two users to the channel                   
    channel_join(user1_credentials['token'], channel1_id['channel_id'])

    owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}

    user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
    channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

    assert isinstance(channel_contents['name'], str)

    assert isinstance(channel_contents['owner_members'], list)
    assert isinstance(channel_contents['owner_members'][0], dict)
    assert isinstance(channel_contents['owner_members'][0]['u_id'], int)
    assert isinstance(channel_contents['owner_members'][0]['name_first'], str)
    assert isinstance(channel_contents['owner_members'][0]['name_last'], str)

    assert isinstance(channel_contents['all_members'], list)
    assert isinstance(channel_contents['all_members'][0], dict)
    assert isinstance(channel_contents['all_members'][0]['u_id'], int)
    assert isinstance(channel_contents['all_members'][0]['name_first'], str)
    assert isinstance(channel_contents['all_members'][0]['name_last'], str)


def test_channel_details_case():

    clear()
    owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
    user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

    channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel

    # Invite two users to the channel                   
    channel_join(user1_credentials['token'], channel1_id['channel_id'])

    owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}
    user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
    channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

    assert channel_contents == channel_details(user1_credentials['token'], channel1_id['channel_id'])


# def test_channel_details_empty_channel():

#     clear()
#     #login the owner and create channel
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)

#   (owner_credentials['token'], channel1_id['channel_id'])

#     with pytest.raises(AccessError):
#         channel_details(owner_credentials['token'], channel1_id['channel_id']
                        


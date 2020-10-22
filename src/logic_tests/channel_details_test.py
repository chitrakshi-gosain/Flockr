# Created collaboratively by Wed15Team2 2020 T3
# Contributer - Ahmet Karatas

# Iteration 1

from auth import auth_register
from channel import channel_details, channel_join, channel_invite, channel_leave
from channels import channels_create
from other import clear
from error import InputError
from error import AccessError
import pytest

@pytest.fixture
def reset():
    clear()

@pytest.fixture
def users(reset):
    admin_details = auth_register('admin@gmail.com', 'admin_pw', 'admin_firstname', 'admin_lastname')
    owner_details = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')   
    user1_details = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')      

    return {
        'admin': admin_details,
        'owner': owner_details,
        'user1': user1_details
    }

@pytest.fixture
def channels(users):
    owner_credentials = users['owner']
    public_channel = channels_create(owner_credentials['token'], 'channel1_name', True)
    private_channel = channels_create(owner_credentials['token'], 'channel1_name', False)
    return {
        'public': public_channel,
        'private': private_channel
    }

def test_insufficient_parameters(users):
    with pytest.raises(InputError):
        channel_details(None, None)

def test_user_not_authorised(users, channels):

    channel1_id = channels['private']
    user1_credentials = users['user1']      
    with pytest.raises(AccessError):
        channel_details(user1_credentials['token'], channel1_id['channel_id'])


def test_channel_id_not_valid(users):
    owner_credentials = users['owner']

    invalid_channel_id = -1 
    with pytest.raises(InputError):
        channel_details(owner_credentials['token'], invalid_channel_id)


def test_token_invalid(users, channels):
    channel1_id = channels['private']

    with pytest.raises(AccessError):
        channel_details('incorrect_user1_token', channel1_id['channel_id'])

def test_return_type(users, channels):
    owner_credentials = users['owner']
    user1_credentials = users['user1']      

    channel1_id = channels['public']
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


def test_channel_details_case(users, channels):

    owner_credentials = users['owner']
    user1_credentials = users['user1']      

    channel1_id = channels['public']
    # Invite two users to the channel                   
    channel_join(user1_credentials['token'], channel1_id['channel_id'])
    owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}
    user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
    channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

    assert channel_contents == channel_details(user1_credentials['token'], channel1_id['channel_id'])

def test_channel_details_empty_channel(users, channels):
    admin_credentials = users['admin']
    owner_credentials = users['owner']
    channel1_id = channels['public']
    channel_leave(owner_credentials['token'], channel1_id['channel_id'])

    channel_contents = {'name': 'channel1_name', 'owner_members': [], 'all_members': []}
    assert channel_contents == channel_details(admin_credentials['token'], channel1_id['channel_id'])
                        


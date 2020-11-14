'''
Created collaboratively by Wed15Team2 2020 T3
Contributor - Ahmet Karatas

Iteration 1
'''

import pytest
from channel import channel_details, channel_join, channel_invite, channel_leave
from error import InputError
from error import AccessError

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> channel_details(token, channel_id) return {name, owner_memers, all_members}
-> channel_join(token, channel_id) return {}
-> channel_invite(token, channel_id, u_id) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> reset
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: InputError
    -> Channel ID is not a valid channel
Error type: AccessError
    -> Authorised user is not a member of channel with channel_id
'''

def test_user_not_authorised(initialise_user_data, initialise_channel_data):

    channel1_id = initialise_channel_data['owner_priv']
    user1_credentials = initialise_user_data['user1']
    with pytest.raises(AccessError):
        channel_details(user1_credentials['token'], channel1_id['channel_id'])


def test_channel_id_not_valid(initialise_user_data):
    owner_credentials = initialise_user_data['owner']

    invalid_channel_id = -1
    with pytest.raises(InputError):
        channel_details(owner_credentials['token'], invalid_channel_id)


def test_token_invalid(initialise_user_data, initialise_channel_data):
    channel1_id = initialise_channel_data['owner_priv']

    with pytest.raises(AccessError):
        channel_details('incorrect_user1_token', channel1_id['channel_id'])

def test_return_type(initialise_user_data, initialise_channel_data):
    user1_credentials = initialise_user_data['user1']
    channel1_id = initialise_channel_data['owner_publ']
    # Invite two initialise_user_data to the channel
    channel_join(user1_credentials['token'], channel1_id['channel_id'])

    channel_information = channel_details(user1_credentials['token'], channel1_id['channel_id'])

    assert isinstance(channel_information, dict)

    assert isinstance(channel_information['name'], str)

    assert isinstance(channel_information['owner_members'], list)
    assert isinstance(channel_information['owner_members'][0], dict)
    assert isinstance(channel_information['owner_members'][0]['u_id'], int)
    assert isinstance(channel_information['owner_members'][0]['name_first'], str)
    assert isinstance(channel_information['owner_members'][0]['name_last'], str)

    assert isinstance(channel_information['all_members'], list)
    assert isinstance(channel_information['all_members'][0], dict)
    assert isinstance(channel_information['all_members'][0]['u_id'], int)
    assert isinstance(channel_information['all_members'][0]['name_first'], str)
    assert isinstance(channel_information['all_members'][0]['name_last'], str)

def test_channel_details_case(initialise_user_data, initialise_channel_data):

    owner_credentials = initialise_user_data['owner']
    user1_credentials = initialise_user_data['user1']

    channel1_id = initialise_channel_data['owner_publ']
    # Invite two initialise_user_data to the channel
    channel_join(user1_credentials['token'], channel1_id['channel_id'])
    owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_first', 'name_last': 'owner_last', 'profile_img_url': '',}
    user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_first', 'name_last': 'user1_last', 'profile_img_url': '',}
    channel_contents = {'name': 'owner_public', 'owner_members': [owner], 'all_members': [owner, user1]}

    assert channel_contents == channel_details(user1_credentials['token'], channel1_id['channel_id'])

def test_channel_details_empty_channel(initialise_user_data, initialise_channel_data):
    admin_credentials = initialise_user_data['admin']
    owner_credentials = initialise_user_data['owner']
    channel1_id = initialise_channel_data['owner_publ']
    channel_leave(owner_credentials['token'], channel1_id['channel_id'])

    channel_contents = {'name': 'owner_public', 'owner_members': [], 'all_members': []}
    assert channel_contents == channel_details(admin_credentials['token'], channel1_id['channel_id'])

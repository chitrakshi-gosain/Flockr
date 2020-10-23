# '''
# Created collaboratively by Wed15GrapeTeam2 2020 T3
# Contributor - YOUR NAME HERE

# Iteration 2
# '''

# import json
# import requests
# import pytest

# '''
# ****************************BASIC TEMPLATE******************************
# '''

# '''
# APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
# json.dumps({RETURN VALUE})
# -> APP.route(.....) return json.dumps({...})
# '''

# '''
# FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
# -> reset
# -> url
# -> ...
# '''

# '''
# EXCEPTIONS
# Error type: InputError
#     -> ..
# Error type: AccessError
#     -> ..
# '''

# def test_url(url):
#     '''
#     A simple sanity test to check that the server is set up properly
#     '''

#     assert url.startswith("http")


# def test_insufficient_parameters():
#     clear()
#     with pytest.raises(InputError):
#         channel_details(None, None)

# def test_user_not_authorised():

#     clear()
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')
#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

#     user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1
#     with pytest.raises(AccessError):
#         channel_details(user1_credentials['token'], channel1_id['channel_id'])


# def test_channel_id_not_valid():
#     clear()
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
#     user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)

#     invalid_channel_id = -1 
#     with pytest.raises(InputError):
#         channel_details(owner_credentials['token'], invalid_channel_id)


# def test_token_invalid():
#     clear()

#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register owner
#     user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', False)

#     with pytest.raises(AccessError):
#         channel_details('incorrect_user1_token', channel1_id['channel_id'])

# def test_return_type():
#     clear()
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
#     user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel

#     # Invite two users to the channel                   
#     channel_join(user1_credentials['token'], channel1_id['channel_id'])

#     owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}

#     user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
#     channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

#     assert isinstance(channel_contents['name'], str)

#     assert isinstance(channel_contents['owner_members'], list)
#     assert isinstance(channel_contents['owner_members'][0], dict)
#     assert isinstance(channel_contents['owner_members'][0]['u_id'], int)
#     assert isinstance(channel_contents['owner_members'][0]['name_first'], str)
#     assert isinstance(channel_contents['owner_members'][0]['name_last'], str)

#     assert isinstance(channel_contents['all_members'], list)
#     assert isinstance(channel_contents['all_members'][0], dict)
#     assert isinstance(channel_contents['all_members'][0]['u_id'], int)
#     assert isinstance(channel_contents['all_members'][0]['name_first'], str)
#     assert isinstance(channel_contents['all_members'][0]['name_last'], str)


# def test_channel_details_case():

#     clear()
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')             # Register user_1
#     user1_credentials = auth_register('user1@gmail.com', 'user1_pw', 'user1_firstname', 'user1_lastname')                # Register user_1

#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)                                 # create a public channel

#     # Invite two users to the channel                   
#     channel_join(user1_credentials['token'], channel1_id['channel_id'])

#     owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}
#     user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
#     channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

#     assert channel_contents == channel_details(user1_credentials['token'], channel1_id['channel_id'])


# def test_channel_details_empty_channel():

#     clear()
#     admin_credentials = auth_register('admin@gmail.com', 'admin_pw', 'admin_firstname', 'admin_lastname')
#     owner_credentials = auth_register('owner@gmail.com', 'owner_pw', 'owner_firstname', 'owner_lastname')            
#     channel1_id = channels_create(owner_credentials['token'], 'channel1_name', True)
#     channel_leave(owner_credentials['token'], channel1_id['channel_id'])

#     channel_contents = {'name': 'channel1_name', 'owner_members': [], 'all_members': []}
#     assert channel_contents == channel_details(admin_credentials['token'], channel1_id['channel_id'])

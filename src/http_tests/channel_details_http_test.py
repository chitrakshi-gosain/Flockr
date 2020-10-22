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

# # def test_url(url):
# #     '''
# #     A simple sanity test to check that the server is set up properly
# #     '''
# #     assert url.startswith("http")

# # def test_something(url):
# #     '''
# #     ADD DOCSTRING HERE
# #     '''

# def test_successful_login_with_everything_valid(url, initialise_user_data):
#     '''
#     Tests that App.route("/auth/login", methods=['POST']) logs-in  the
#     user successfully
#     '''

#     test_user_0 = initialise_user_data['user0']

#     logout_response = requests.post(f"{url}/auth/logout", json={
#         'token': test_user_0['token']
#     })
#     assert logout_response.status_code == 200

#     login_response = requests.post(f"{url}/auth/login", json={
#         'email': 'user0@email.com',
#         'password': 'user0_pass1!'
#     })
#     assert login_response.status_code == 200

# def test_insufficient_parameters(initialise_user_data):
#     user0 = initialise_user_data['user0']
#     response = requests.get(f"{url}/channel/details", params={
#         'token': user0['token'],
#         'channel_id': None
#     })
#     assert response.status_code == 400


# def test_user_not_authorised(initialise_user_data, initialise_channel_data):
#     user0 = initialise_user_data['user0']
#     channel1_id = initialise_channel_data['user1_priv']
#     response = requests.get(f"{url}/channel/details", params={
#         'token': user0['token'],
#         'channel_id': channel1_id['channel_id']
#     })
#     assert response.status_code == 400

# def test_channel_id_not_valid(initialise_user_data):
#     owner_credentials = initialise_user_data['owner']

#     invalid_channel_id = -1 
#     with pytest.raises(InputError):
#         channel_details(owner_credentials['token'], invalid_channel_id)


# def test_token_invalid(initialise_user_data, initialise_channel_data):
#     channel1_id = initialise_channel_data['private']

#     with pytest.raises(AccessError):
#         channel_details('incorrect_user1_token', channel1_id['channel_id'])

# def test_return_type(initialise_user_data, initialise_channel_data):
#     owner_credentials = initialise_user_data['owner']
#     user1_credentials = initialise_user_data['user1']      

#     channel1_id = initialise_channel_data['public']
#     # Invite two initialise_user_data to the channel                   
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


# def test_channel_details_case(initialise_user_data, initialise_channel_data):

#     owner_credentials = initialise_user_data['owner']
#     user1_credentials = initialise_user_data['user1']      

#     channel1_id = initialise_channel_data['public']
#     # Invite two initialise_user_data to the channel                   
#     channel_join(user1_credentials['token'], channel1_id['channel_id'])
#     owner = {'u_id': owner_credentials['u_id'], 'name_first': 'owner_firstname', 'name_last': 'owner_lastname'}
#     user1 = {'u_id': user1_credentials['u_id'], 'name_first': 'user1_firstname', 'name_last': 'user1_lastname'}
#     channel_contents = {'name': 'channel1_name', 'owner_members': [owner], 'all_members': [owner, user1]}

#     assert channel_contents == channel_details(user1_credentials['token'], channel1_id['channel_id'])

# def test_channel_details_empty_channel(initialise_user_data, initialise_channel_data):
#     admin_credentials = initialise_user_data['admin']
#     owner_credentials = initialise_user_data['owner']
#     channel1_id = initialise_channel_data['public']
#     channel_leave(owner_credentials['token'], channel1_id['channel_id'])

#     channel_contents = {'name': 'channel1_name', 'owner_members': [], 'all_members': []}
#     assert channel_contents == channel_details(admin_credentials['token'], channel1_id['channel_id'])
                        


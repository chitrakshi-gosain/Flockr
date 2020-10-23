# '''
# Created collaboratively by Wed15GrapeTeam2 2020 T3
# Contributor -

# Iteration 1
# '''

# import json
# import requests
# import pytest

# '''
# ****************************BASIC TEMPLATE******************************
# '''

# '''
# FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
# -> is_user_in_channel(url, user_id, token, channel_id) return amount of times u_id was found in channel
# -> test_channel_join_basic()
# -> test_channel_join_invalid_channel()
# -> test_channel_join_private_user()
# -> test_channel_join_private_admin()
# -> test_channel_join_invalid_token()
# -> test_channel_join_already_member()
# '''

# '''
# ----channel_join Documentation----
# Parameters:
# (token, channel_id)

# Return Type:
# {}

# Exceptions:
#     InputError (400) when:
#         -> Channel ID is not a valid channel
#     AccessError (400) when:
#         -> channel_id refers to a channel that is private (when the authorised user is not a global owner)

# Description: Given a channel_id of a channel that the
#              authorised user can join, adds them to that channel
# '''

# # Jordan Huynh (z5169771)
# # Wed15 Grape 2

# def get_messages(url, admin_token):
#     messages = requests.get(url + "/search", params = {
#         "token": admin_token,
#         "query_str": ""
#     }).json()
#     return messages

# def test_user_not_authorised(url, reset, initialise_user_data, initialise_channel_data):

#     send_input = {
#         "token": initialise_user_data['user1']['token'],
#         "channel_id": initialise_channel_data['admin_priv']['channel_id'],
#         "message": "Sample message"
#     }
#     response = requests.post(url + "/message/send", json=send_input)
#     assert response.status_code == 400


# def test_channel_id_not_valid(url, reset, initialise_user_data, initialise_channel_data):

#     send_input = {
#         "token": initialise_user_data['admin']['token'],
#         "channel_id": -1,
#         "message": "Sample message"
#     }
#     response = requests.post(url + "/message/send", json=send_input)
#     assert response.status_code == 400


# def test_token_invalid(url, reset, initialise_user_data, initialise_channel_data):

#     send_input = {
#         "token": " ",
#         "channel_id": initialise_channel_data['admin_publ']['channel_id'],
#         "message": "Sample message"
#     }
#     response = requests.post(url + "/message/send", json=send_input)
#     assert response.status_code == 400

# # def test_return_type(url, reset, initialise_user_data, initialise_channel_data):

# #     send_input = {
# #         "token": initialise_user_data['admin']['token'],
# #         "channel_id": initialise_channel_data['admin_publ']['channel_id'],
# #         "message": "Sample message"
# #     }
# #     response = requests.post(url + "/message/send", json=send_input)
# #     assert response.status_code == 200

# #     messages = get_messages(url, initialise_user_data['admin']['token'])
# #     assert isinstance(messages['messages'], list)
# #     assert isinstance(messages['messages'][0], dict)
# #     assert isinstance(messages['messages'][0]['message_id'], int)
# #     assert isinstance(messages['messages'][0]['u_id'], int)
# #     assert isinstance(messages['messages'][0]['message'], str)
# #     assert isinstance(messages['messages'][0]['message'], object)

# # def test_sample(url, reset, initialise_user_data, initialise_channel_data):
# #     #join channel
# #     requests.post(url + "/channel/join", json={
# #         "token": initialise_user_data['user1']['token'],
# #         "channel_id": initialise_channel_data['admin_publ']['channel_id']
# #     })
# #     # admin message1
# #     send_input = {
# #         "token": initialise_user_data['admin']['token'],
# #         "channel_id": initialise_channel_data['admin_publ']['channel_id'],
# #         "message": "Hey, how are you"
# #     }
# #     response = requests.post(url + "/message/send", json=send_input)
# #     assert response.status_code == 200

# #     # user1 message1
# #     send_input = {
# #         "token": initialise_user_data['admin']['token'],
# #         "channel_id": initialise_channel_data['admin_publ']['channel_id'],
# #         "message": "Good thank you, how are you!"
# #     }
# #     response = requests.post(url + "/message/send", json=send_input)
# #     assert response.status_code == 200
# #     message_id = response.json()

# #     # admin message 2
# #     send_input = {
# #         "token": initialise_user_data['admin']['token'],
# #         "channel_id": initialise_channel_data['admin_publ']['channel_id'],
# #         "message": "Very well, thanks."
# #     }
# #     response = requests.post(url + "/message/send", json=send_input)
# #     assert response.status_code == 200

# #     messages = get_messages(url, initialise_user_data['admin']['token'])
# #     for message in messages['messages']:
# #         if message['message_id'] == message_id['message_id']:
# #             assert message['message'] == "Good thank you, how are you!"

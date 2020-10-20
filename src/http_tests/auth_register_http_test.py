'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Chitrakshi Gosain

Iteration 2
'''

import json
import requests
import pytest
from error import InputError

# need to plan how to format this
'''
****************************BASIC TEMPLATE******************************
'''

# def test_url(url):
#     '''
#     A simple sanity test to check that your server is set up properly
#     '''
#     assert url.startswith("http")

# def test_successful_registration(reset, url):
#     '''
#     ADD DOCSTRING HERE
#     '''

#     requests.post(f"{url}/auth/register", json={
#         'email': 'user0@email.com',
#         'password': 'user0_pass1!',
#         'name_first': 'user0_first',
#         'name_last': 'user0_last'
#     })

# def test_invalid_registration(reset, url):

#     user0 = {
#         'email': 'user0_email.com',
#         'password': 'user0_pass1!',
#         'name_first': 'user0_first',
#         'name_last': 'user0_last'
#     }

#     # Tests that auth_register raises an InputError when an invalid
#     # email is passed as one of the parameters
#     with pytest.raises(InputError):
#         requests.post(f"{url}/auth/register", json=user0)

#     # Tests that auth_register raises an InputError when a name_first is
#     # less than 1 characters long
#     user0['name_first'] = ''
#     with pytest.raises(InputError):
#         requests.post(f"{url}/auth/register", json=user0)
    
#     # Tests that auth_register raises an InputError when a name_last is
#     # less than 1 characters long
#     user0['name_first'] = 'user0_first'
#     user0['name_last'] = ''
#     with pytest.raises(InputError):
#         requests.post(f"{url}/auth/register", json=user0)

#     # Tests that auth_register raises an InputError when a user tries to
#     # register with an existing email-id in database registered with
#     # another user
#     requests.post(f"{url}/auth/register", json=user0)
#     with pytest.raises(InputError):
#         requests.post(f"{url}/auth/register", json=user0)

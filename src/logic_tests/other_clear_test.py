'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - Jordan Hunyh

Iteration 2
'''

import pytest
from error import AccessError
from channel import channel_details
from other import clear

'''
FUNCTIONS_USED_FOR_THIS_TEST(PARAMETERS) return {RETURN_VALUES}:
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> channels_create(token, name. is_public) return {channel_id}
-> clear() return {}
-> channel_details(token, channel_id) return 
   {name, owner_memers, all_members}
-> channel_join(token, channel_id) return {}
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/logic_tests/conftest.py)
-> initialise_user_data
-> initialise_channel_data
'''

'''
EXCEPTIONS
Error type: AccessError
    -> token passed in is not a valid token
'''

def test_check_empty(initialise_user_data, initialise_channel_data):

    token = initialise_user_data['admin']['token']
    channel_id = initialise_channel_data['admin_publ']['channel_id']

    details = channel_details(token, channel_id)

    assert details # not empty

    clear()
    with pytest.raises(AccessError): #expect AccessError as all data has been cleared
        assert channel_details(token, channel_id)

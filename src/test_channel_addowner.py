from channel import *
from channels import *

# channel_addowner should add the user with the provided u_id to the list of owners of a channel with the provided channel_id
# assumes that u_id is already a member of the channel
def test_channel_addowner():
from auth import auth_*
from channel import channel_*
from channels import channels_*
from other import clear
import pytest

# Sets up various user sample data for testing purposes
def initialise_user_data():
    # Ensures any currently existing data is removed
    clear()

    # Register users:
    # Descriptive test data
    owner_details = auth_register('owner@email.com', 'owner_pass', 'owner_first', 'owner_last')
    user1_details = auth_register('user1@email.com', 'user1_pass', 'user1_first', 'user1_last')
    user2_details = auth_register('user2@email.com', 'user2_pass', 'user2_first', 'user2_last')
    user3_details = auth_register('user3@email.com', 'user3_pass', 'user3_first', 'user3_last')
    user4_details = auth_register('user4@email.com', 'user4_pass', 'user4_first', 'user4_last')
    user5_details = auth_register('user5@email.com', 'user5_pass', 'user5_first', 'user5_last')

    # Realistic test data
    john_details = auth_register('johnsmith@gmail.com', 'qwertyuiop', 'John', 'Smith')
    jane_details = auth_register('janesmith@hotmail.com', 'mydateofbirth', 'Jane', 'Smith')
    noah_details = auth_register('noah_navarro@yahoo.com', 'aP00RPassWord', 'Noah', 'Navarro')
    ingrid_details = auth_register('ingrid.cline@gmail.com', '572o75630', 'Ingrid', 'Cline')
    donald_details = auth_register('donaldrichards@gmail.com', 'kjdfg;h;;df', 'Donald', 'Richards')

    # Returns user data that is implementation dependent (id, token)
    return {
        'owner': owner_details,
        'user1': user1_details,
        'user2': user2_details,
        'user3': user3_details,
        'user4': user4_details,
        'user5': user5_details,
        'john': john_details,
        'jane': jane_details,
        'noah': noah_details,
        'ingrid': ingrid_details,
        'donald': donald_details
    }





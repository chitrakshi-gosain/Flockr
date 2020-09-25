import auth
import channel
import channels

# Sets up various user sample data for testing purposes
def initialise_user_data():
	# Register users:
	# Descriptive test data
	(owner_id, owner_token) = auth_register('owner@email.com', 'owner_pass', 'owner_first', 'owner_last')
	(user1_id, user1_token) = auth_register('user1@email.com', 'user1_pass', 'user1_first', 'user1_last')
	(user2_id, user2_token) = auth_register('user2@email.com', 'user2_pass', 'user2_first', 'user2_last')
    (user3_id, user3_token) = auth_register('user3@email.com', 'user3_pass', 'user3_first', 'user3_last')
    (user4_id, user4_token) = auth_register('user4@email.com', 'user4_pass', 'user4_first', 'user4_last')
	(user5_id, user5_token) = auth_register('user5@email.com', 'user5_pass', 'user5_first', 'user5_last')

	# Realistic test data
	(john_id, john_token) = auth_register('johnsmith@gmail.com', 'qwertyuiop', 'John', 'Smith')
	(jane_id, jane_token) = auth_register('janesmith@hotmail.com', 'mydateofbirth', 'Jane', 'Smith')
	(noah_id, noah_token) = auth_register('noah_navarro@yahoo.com', 'aP00RPassWord', 'Noah', 'Navarro')
	(ingrid_id, ingrid_token) = auth_register('ingrid.cline@gmail.com', '572o75630', 'Ingrid', 'Cline')
	(donald_id, donald_token) = auth_register('donaldrichards@gmail.com', 'kjdfg;h;;df', 'Donald', 'Richards')

	# Returns user data that is implementation dependent
	return {
		'owner': {'id': owner_id, 'token': owner_token},
		'user1': {'id': user1_id, 'token': user1_token},
		'user2': {'id': user2_id, 'token': user2_token},
		'user3': {'id': user3_id, 'token': user3_token},
		'user4': {'id': user4_id, 'token': user4_token},
		'user5': {'id': user5_id, 'token': user5_token},
		'john': {'id': john_id, 'token': john_token},
		'jane': {'id': jane_id, 'token': jane_token},
		'noah': {'id': noah_id, 'token': noah_token},
		'ingrid': {'id': ingrid_id, 'token': ingrid_token},
		'donald': {'id': donald_id, 'token': donald_token}
	}

# Creating channel with valid data
def test_channels_create_valid_simple1():
	# Creating a basic public channel
	users = initialise_user_data()	
	basic_channel_id = channels_create(users['owner']['token'], 'A Basic Channel', true)

	# Checks that channels_create has returned a valid id (integer value)
	assert isinstance(basic_channel_id, int)
	
	# Checks that channel details have all been set correctly
	basic_channel_details = channel_details(users['owner']['token'], basic_channel_id)

	assert basic_channel_details['name'] == 'A Basic Channel'
	assert basic_channel_details['owner_members'][0]['u_id'] == users['owner']['id']
	assert basic_channel_details['owner_members'][0]['name_first'] == 'owner_first'
	assert basic_channel_details['owner_members'][0]['name_last'] == 'owner_last'
	assert basic_channel_details['all_members'][0]['u_id'] == users['owner']['id']
	assert basic_channel_details['all_members'][0]['name_first'] == 'owner_first'
	assert basic_channel_details['all_members'][0]['name_last'] == 'owner_last'

# Creating channel with empty string name
# Creating channel with too large of a name
# Creating two channels with the same name
# Non-existant user creating a channel
# Logged out user creating channel
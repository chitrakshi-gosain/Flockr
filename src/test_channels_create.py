import auth
import channel
import channels

# Sets up various user sample data for testing purposes
def initialise_user_data():
	# Register users:
	# Descriptive test data
	(owner_id, owner_token) = auth_register("owner@email.com", "owner_pass", "owner_first", "owner_last")
	(user1_id, user1_token) = auth_register("user1@email.com", "user1_pass", "user1_first", "user1_last")
	(user2_id, user2_token) = auth_register("user2@email.com", "user2_pass", "user2_first", "user2_last")
    (user3_id, user3_token) = auth_register("user3@email.com", "user3_pass", "user3_first", "user3_last")
    (user4_id, user4_token) = auth_register("user4@email.com", "user4_pass", "user4_first", "user4_last")
	(user5_id, user5_token) = auth_register("user5@email.com", "user5_pass", "user5_first", "user5_last")

	# Realistic test data
	(john_id, john_token) = auth_register("johnsmith@gmail.com", "qwertyuiop", "John", "Smith")
	(jane_id, jane_token) = auth_register("janesmith@hotmail.com", "mydateofbirth", "Jane", "Smith")
	(noah_id, noah_token) = auth_register("noah_navarro@yahoo.com", "aP00RPassWord", "Noah", "Navarro")
	(ingrid_id, ingrid_token) = auth_register("ingrid.cline@gmail.com", "572o75630", "Ingrid", "Cline")
	(donald_id, donald_token) = auth_register("donaldrichards@gmail.com", "kjdfg;h;;df", "Donald", "Richards")

	return {
		'owner': [owner_id, owner_token],
		'user1': [user1_id, user1_token],
		'user2': [user2_id, user2_token],
		'user3': [user3_id, user3_token],
		'user4': [user4_id, user4_token],
		'user5': [user5_id, user5_token],
		'john': [john_id, john_token],
		'jane': [jane_id, jane_token],
		'noah': [noah_id, noah_token],
		'ingrid': [ingrid_id, ingrid_token],
		'donald': [donald_id, donald_token]
	}

# Creating channel validly
def test_channels_create_valid_simple():
	# Creating a basic public channel
	users = initialise_user_data()
	channels_create(users['owner'][1], "A Basic Channel", true)

# Non-Existent user creating channel
# Logged out user creating channel
# Creating channel with no name
# Creating channel with too large of a name
# Creating two channels with the same name
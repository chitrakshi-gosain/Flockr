import data

def is_user_authorised(token):
    #checks token, returns true/false
    pass

def get_user_info(u_id):
    for user in data.data['users']:
        if user['u_id'] == u_id:
            return user

#more functions

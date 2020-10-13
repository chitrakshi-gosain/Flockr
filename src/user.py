'''
Created collaboratively by Wed15Team2 2020 T3
Contributer - Cyrus Wilkie, Chitrakshi Gosain, Joseph Knox

Iteration 2
'''

# import stuff here


# edit basic template to fit this file

'''
****************************BASIC TEMPLATE******************************
'''

'''
FUNCTIONS_IN_THIS FILE(PARAMETERS) return {RETURN_VALUES}:
-> user_profile(token, u_id) return {user}
-> user_profile_setname(token, name_first, name_last) return {}
-> user_profile_setemail(token, email) return {}
-> user_profile_sethandle(toke, handle_str) return {}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> token: string
    -> u_id: inetger
    -> user: dictionary containing u_id, email, name_first, name_last,
             handle_str
    -> name_first: string
    -> name_last: string
    -> email: string
    -> handle_str: string
'''

'''
EXCEPTIONS
    * user_profile
        Error type: InputError
            -> insufficient parameters
            -> user with u_id is not a valid_user
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_setname
        Error type: InputError
            -> insufficient parameters
            -> name_first is not between 1 and 50 characters inclusively
               in length
            -> name_last is not between 1 and 50 characters inclusively
               in length
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_setemail
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email address is already being used by another user
        Error type: AccessError
            -> token passed in is not a valid token
    * user_profile_sethandle
        Error type: InputError
            -> insufficient parameters
            -> handle_str must be between 3 and 20 characters
            -> handle is already being used by another user
        Error type: AccessError
            -> token passed in is not a valid token
'''

'''
KEEP IN MIND:
-> allow multiple session log-ins,
   * for this make a data.data['valid_tokens'] dict in data.py, have
   tokens as key, and value as u_id this way we can keep track of
   multiple logins very easily, but dont do it now everyone will have to
   change implementation, do it after we are done merging all branches
   once, so if anything ever goes wrong we have A BACKUP. also, this
   aint imp for itr 1 so dont stress. :)
'''

def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    '''
    DESCRIPTION:
    Updates the authorised user's email address

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorised)
        -> email : email of a user
    '''

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    DESCRIPTION:
    Updates the authorised user's handle (i.e. display name)

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorised)
        -> handle_str : handle of a user
    '''

    return {
    }

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
-> auth_register(email, password, name_first, name_last) return
   {u_id, token}
-> auth_login(email,password) return {u_id, token}
-> auth_logout(token) return {is_sucess}
'''

'''
DATA TYPES  OF ALL PARAMETERS / RETURN VALUES
    -> email: string
    -> password: string
    -> name_first: string
    -> name_last: string
    -> token: string
    -> u_id: inetger
    -> is_success: boolean
'''

'''
EXCEPTIONS
    * auth_login
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email entered does not belong to a user
            -> password is not correct
    * auth_logout
        Error type: InputError
            -> insufficient parameters
        Error type: AccessError
            -> token passed in is not a valid token
    * auth_register
        Error type: InputError
            -> insufficient parameters
            -> email entered is not a valid email
            -> email address is already being used by another user
            -> password entered is less than 6 characters long or more
               than 32 characters long
            -> name_first is not between 1 and 50 characters inclusively
               in length
            -> name_last is not between 1 and 50 characters inclusively
               in length
'''

'''
KEEP IN MIND:
-> make one function to check if user is registered and use it for both
   re-registration check and registered before login check
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
    '''
    DESCRIPTION:
    here

    PARAMETERS:
        -> param : elab what param is eg email : email of a user

    RETURN VALUES:
        -> return_vales : elab it eg u_id : user-id of the user
    '''

    return {
    }

def user_profile_setemail(token, email):
    '''
    DESCRIPTION:
    here

    PARAMETERS:
        -> param : elab what param is eg email : email of a user

    RETURN VALUES:
        -> return_vales : elab it eg u_id : user-id of the user
    '''

    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }
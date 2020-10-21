'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributors - Chitrakshi Gosain, Joseph Knox, Cyrus Wilkie,
               Jordan Hunyh, Ahmet Karatas

Iteration 2
'''

from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
# import sys
from auth import auth_login, auth_register, auth_logout
# from channel import channel_invite, channel_details, channel_messages, \
#     channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
# from message import message_send, message_remove, message_edit
from  user import user_profile, user_profile_setname, user_profile_setemail, \
#     user_profile_sethandle  
from other import users_all, admin_userpermission_change, search, clear

# need to plan how to write things here
'''
**************************BASIC TEMPLATE****************************
'''

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# @APP.route("/auth/login", methods=['POST'])
# def auth_login_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/auth/logout", methods=['POST'])
# def auth_logout_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/auth/register", methods=['POST'])
# def auth_register_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/invite", methods=['POST'])
# def channel_invite_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/details", methods=['GET'])
# def channel_details_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/messages", methods=['GET'])
# def channel_messages_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/leave", methods=['POST'])
# def channel_leave_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/join", methods=['POST'])
# def channel_join_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/addowner", methods=['POST'])
# def channel_addowner_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channel/removeowner", methods=['POST'])
# def channel_removeowner_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

@APP.route("/channels/list", methods=['GET'])
def channels_list_route():
    '''
    DESCRIPTION:
    Provide a list of all channels (and
    their associated details) that the
    authorised user is part of

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> AccessError: Invalid token
    '''

    token = request.args.get('token')

    return dumps(channels_list(token))
    

@APP.route("/channels/listall", methods=['GET'])
def channels_listall_route():
    '''
    DESCRIPTION:
    Provide a list of all channels (and
    their associated details) that the
    authorised user is part of

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> AccessError: Invalid token
    '''

    token = request.args.get('token')

    return dumps(channels_listall(token))

@APP.route("/channels/create", methods=['POST'])
def channels_create_route():
    '''
    DESCRIPTION:
    Creates a new channel with that name
    that is either a public or private channel

    PARAMETERS:
        -> token
        -> name: Name of channel to be created
        -> is_public: Whether the channel is public

    RETURN VALUES:
        -> {channels}

    EXCEPTIONS:
        -> InputError when any of:
            - Name is more than 20 characters long
    '''
    
    input_data = request.get_json()

    return dumps(channels_create(input_data['token'], input_data['name'], input_data['is_public']))

# @APP.route("/message/send", methods=['POST'])
# def message_send_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/message/remove", methods=['DELETE'])
# def message_remove_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/message/edit", methods=['PUT'])
# def message_edit_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

@APP.route("/user/profile", methods=['GET'])
def user_profile_route():
    '''
    DESCRIPTION:
    For a valid user, returns information about
    their user_id, email, first name, last name,
    and handle

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> u_id : user id of a user

    RETURN VALUES:
        -> user : dictionary containing u_id, email, name_first,
                  name_last, handle_str of the user
    '''
    
    token = request.args.get('token')
    u_id = request.args.get('u_id')

    return dumps(user_profile(token, u_id))

# @APP.route("/user/profile/setname", methods=['PUT'])
# def user_profile_setname_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/user/profile/setemail", methods=['PUT'])
# def user_profile_setemail_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/user/profile/sethandle", methods=['PUT'])
# def user_profile_sethandle_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

@APP.route("/users/all", methods=['GET'])
def users_all_route():
    '''
    DESCRIPTION:
    Returns a list of all users and
    their associated details

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> {users}

    EXCEPTIONS:
        -> AccessError: Invalid token
    '''
    
    token = request.args.get('token')

    return dumps(users_all(token))

# @APP.route("/admin/userpermission/change", methods=['POST'])
# def change_userpermission_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/search", methods=['GET'])
# def search_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/clear", methods=['DELETE'])
# def clear_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# DO NOT EDIT ANYTHING BELOW THIS LINE

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
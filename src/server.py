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
import sys
from auth import auth_login, auth_register, auth_logout
from channel import channel_invite, channel_details, channel_messages, \
    channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from message import message_send, message_remove, message_edit
from  user import user_profile, user_profile_setname, user_profile_setemail, \
    user_profile_sethandle  
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

@APP.route("/auth/login", methods=['POST'])
def auth_login_route():
    '''
    DONT COMMIT THIS YET
    '''
    
    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_login(email, password))


@APP.route("/auth/logout", methods=['POST'])
def auth_logout_route():
    '''
    ADD DOCSTRING HERE
    '''

    payload = request.get_json()
    token = payload['token']

    return dumps(auth_logout(token))

@APP.route("/auth/register", methods=['POST'])
def auth_register_route():
    '''
    ADD DOCSTRING HERE
    '''

    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']

    return dumps(auth_register(email, password, name_first, name_last))

# @APP.route("/channel/invite", methods=['POST'])
# def channel_invite_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

@APP.route("/channel/details", methods=['GET'])
def channel_details_route():
    '''
    ADD DOCSTRING HERE
    '''

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel_details(token, channel_id))

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_route():
    '''
    ADD DOCSTRING HERE
    '''

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    return dumps(channel_messages(token, channel_id, start))

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

# @APP.route("/channels/list", methods=['GET'])
# def channels_list_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channels/listall", methods=['GET'])
# def channels_listall_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

# @APP.route("/channels/create", methods=['POST'])
# def channels_create_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

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

# @APP.route("/user/profile", methods=['GET'])
# def user_profile_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

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

# @APP.route("/users/all", methods=['GET'])
# def users_all_route():
#     '''
#     ADD DOCSTRING HERE
#     '''
#     pass

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

@APP.route("/clear", methods=['DELETE'])
def clear_route():
    '''
    THIS IS NOT OFFICIAL, THIS IS JUST TO GET AUTH TESTS WORKING
    THIS FUNCTION IS OFFICIALLY IMPLEMENTED BY Jordan Hunyh
    '''
    
    clear()
    return dumps({})

# Example, it is associated with echo_http_test.py, do not remove it
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
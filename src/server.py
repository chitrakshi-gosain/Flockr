import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

import channel
import channels
import auth
import message
import other
import user

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

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/login", methods=['POST'])
def http_login():
    email = request.get_json()['email']
    password = request.get_json()['password']

    return dumps(auth.auth_login(email, password))

@APP.route("/auth/logout", methods=['POST'])
def http_logout():
    token = request.get_json()['token']
    #token = request.args.get('token')

    return dumps(auth.auth_logout(token))

@APP.route("/auth/register", methods=['POST'])
def http_register():
    email = request.get_json()['email']
    password = request.get_json()['password']
    name_first = request.get_json()['name_first']
    name_last = request.get_json()['name_last']

    return dumps(auth.auth_register(email, password, name_first, name_last))

@APP.route("/channel/invite", methods=['POST'])
def http_invite():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])
    u_id = int(request.get_json()['u_id'])

    return dumps(channel.channel_invite(token, channel_id, u_id))

@APP.route("/channel/details", methods=['GET'])
def http_details():
    #token = request.get_json()['token']
    #channel_id = int(request.get_json()['channel_id'])

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel.channel_details(token, channel_id))

@APP.route("/channel/messages", methods=['GET'])
def http_messages():
    #token = request.get_json()['token']
    #channel_id = int(request.get_json()['channel_id'])
    #start = int(request.get_json()['start'])

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    return dumps(channel.channel_messages(token, channel_id, start))

@APP.route("/channel/leave", methods=['POST'])
def http_leave():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])

    return dumps(channel.channel_leave(token, channel_id))

@APP.route("/channel/join", methods=['POST'])
def http_join():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])

    return dumps(channel.channel_join(token, channel_id))

@APP.route("/channel/addowner", methods=['POST'])
def http_addowner():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])
    u_id = int(request.get_json()['u_id'])

    return dumps(channel.channel_addowner(token, channel_id, u_id))

@APP.route("/channel/removeowner", methods=['POST'])
def http_removeowner():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])
    u_id = int(request.get_json()['u_id'])

    return dumps(channel.channel_removeowner(token, channel_id, u_id))

@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    #token = request.get_json()['token']
    token = request.args.get('token')

    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    #token = request.get_json()['token']
    token = request.args.get('token')

    return dumps(channels.channels_listall(token))

@APP.route("/channels/create", methods=['POST'])
def http_create():
    token = request.get_json()['token']
    name = request.get_json()['name']
    is_public = bool(request.get_json()['is_public'])

    return dumps(channels.channels_create(token, name, is_public))

@APP.route("/message/send", methods=['POST'])
def http_send():
    token = request.get_json()['token']
    channel_id = int(request.get_json()['channel_id'])
    message_str = request.get_json()['message']

    return dumps(message.message_send(token, channel_id, message_str))

@APP.route("/message/remove", methods=['DELETE'])
def http_remove():
    token = request.get_json()['token']
    message_id = int(request.get_json()['message_id'])

    return dumps(message.message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    token = request.get_json()['token']
    message_id = int(request.get_json()['message_id'])
    message_str = request.get_json()['message']

    return dumps(message.message_edit(token, message_id, message_str))

@APP.route("/user/profile", methods=['GET'])
def http_profile():
    #token = request.get_json()['token']
    #u_id = int(request.get_json()['u_id'])

    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    return dumps(user.user_profile(token, u_id))

@APP.route("/user/profile/setname", methods=['PUT'])
def http_setname():
    token = request.get_json()['token']
    name_first = request.get_json()['name_first']
    name_last = request.get_json()['name_last']

    return dumps(user.user_profile_setname(token, name_first, name_last))

@APP.route("/user/profile/setemail", methods=['PUT'])
def http_setemail():
    token = request.get_json()['token']
    email = request.get_json()['email']

    return dumps(user.user_profile_setemail(token, email))

@APP.route("/user/profile/sethandle", methods=['PUT'])
def http_sethandle():
    token = request.get_json()['token']
    handle_str = request.get_json()['handle_str']

    return dumps(user.user_profile_sethandle(token, handle_str))

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    #token = request.get_json()['token']
    token = request.args.get('token')

    return dumps(other.users_all(token))

@APP.route("/admin/userpermission/change", methods=['POST'])
def http_userpermission_change():
    token = request.get_json()['token']
    u_id = int(request.get_json()['u_id'])
    permission_id = int(request.get_json()['permission_id'])

    return dumps(other.admin_userpermission_change(token, u_id, permission_id))

@APP.route("/search", methods=['GET'])
def http_search():
    #token = request.get_json()['token']
    #query_str = request.get_json()['query_str']

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    return dumps(other.search(token, query_str))

@APP.route("/clear", methods=['DELETE'])
def http_clear():

    return dumps(other.clear())


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

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

'''
**************************BASIC TEMPLATE****************************
'''

'''
This file contains all the APP.routes required in order to implement the
HTTP Flask server
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
    DESCRIPTION:
    Given a registered user's email and password and generates a valid
    token for the user to remain authenticated

    PARAMETERS:
        -> email : email-id of user
        -> password : password of the user

    RETURN VALUES:
        -> u_id : user-id of the user
        -> token : token to authenticate the user

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email entered does not belong to a user
        -> password is not correct
    '''

    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_login(email, password))


@APP.route("/auth/logout", methods=['POST'])
def auth_logout_route():
    '''
    DESCRIPTION:
    Given an active token, invalidates the token to log the user out. If
    a valid token is given, and the user is successfully logged out, it
    returns true, otherwise false

    PARAMETERS:
        -> token : token of the authenticated user

    RETURN VALUES:
        -> is_success : True if user is successfully logged out,
                        otherwise False
    
    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    payload = request.get_json()
    token = payload['token']

    return dumps(auth_logout(token))

@APP.route("/auth/register", methods=['POST'])
def auth_register_route():
    '''
    DESCRIPTION:
    Given a user's first and last name, email address, and password,
    creates a new account for them and returns a new token for
    authentication in their session. A handle is generated that is the
    concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20
    characters. If the handle is already taken, user's u_id is
    concatenated at the very end, incase this exceeds the length of 20
    characters, the last characters of handle string are adjusted to
    accommodate the user's u_id

    PARAMETERS:
        -> email : email-id of user
        -> password : password of the user
        -> name_first : first name of the user
        -> name_last : last name of the user

    RETURN VALUES:
        -> u_id : user-id of the user
        -> token : token to authenticate the user

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email address is already being used by another user
        -> password entered is less than 6 characters long or more
            than 32 characters long
        -> name_first is not between 1 and 50 characters inclusively
            in length
        -> name_last is not between 1 and 50 characters inclusively
            in length
    '''

    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']

    return dumps(auth_register(email, password, name_first, name_last))

@APP.route("/channel/invite", methods=['POST'])
def channel_invite_route():
    '''
    DESCRIPTION:
    Invites a user (with user id u_id) to join a channel with ID
    channel_id. Once invited the user is added to the channel
    immediately

    PARAMETERS:
        -> token : token of user who called invite
        -> channel_id : id of the channel
        -> u_id : id of the user who is to be invited

    EXCEPTIONS:
    Error type: InputError
        -> channel_id does not refer to a valid channel
        -> u_id does not refer to a valid user
    Error type: AccessError
        -> token passed in is not a valid token
        -> the authorised user is not already a member of the
            channel
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])

    return dumps(channel_invite(token, channel_id, u_id))

@APP.route("/channel/details", methods=['GET'])
def channel_details_route():
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns a list of
    dictionaries which contain the channel's name, its owner members and
    all of its members.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel

    RETURN VALUES:
        -> name : name of the channel
        -> owner_members :  all owner members of the channels
        -> all_members: all members of the channels, includes owners too

    EXCEPTIONS:
    Error type: InputError
        -> Channel is not valid
    Error type: AccessError
        -> token passed in is not a valid token
        -> User is not an authorised member of the channel
    '''

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel_details(token, channel_id))

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_route():
    '''
    DESCRIPTION:
    Given a channel_id that a user is authorised in, returns the
    messages from the start message to the start + 50'th message.

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel
        -> start: the position to start loading the messages

    RETURN VALUES:
        -> messages : messages in the channel
        -> start : start index of messages returned from channel
        -> end : end index of messages returned from channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel is not valid
        -> If start is greater than the number of messages in the
            channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> User is not an authorised member of the channel
    '''

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    return dumps(channel_messages(token, channel_id, start))

@APP.route("/channel/leave", methods=['POST'])
def channel_leave_route():
    '''
    DESCRIPTION:
    Given a channel ID, the user removed as a member of this channel

    PARAMETERS:
        -> token : token of user who is to leave
        -> channel_id : id of the channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> Authorised user is not a member of channel with channel_id
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])

    return dumps(channel_leave(token, channel_id))

@APP.route("/channel/join", methods=['POST'])
def channel_join_route():
    '''
    DESCRIPTION:
    Given a channel_id of a channel that the
    authorised user can join, adds them to that channel

    PARAMETERS:
        -> token : token of user who is to join channel
        -> channel_id : id of the channel

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> channel_id refers to a channel that is private (when the
            authorised user is not a global owner)
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])

    return dumps(channel_join(token, channel_id))

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner_route():
    '''
    DESCRIPTION:
    Make user with user id u_id an owner of the channel
    with channel id channel_id

    PARAMETERS:
        -> token : token for authenticating the user
        -> channel_id : id of channel to be added to
        -> u_id : id of user to be added

    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
        -> When user with user id u_id is already an owner of the
            channel
    Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user is not an owner of the flockr,
           or an owner of this channel
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])

    return dumps(channel_addowner(token, channel_id, u_id))

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner_route():
    '''
    DESCRIPTION:
    Make user with user id u_id no longer an owner of the channel
    with channel id channel_id

    PARAMETERS:
        -> token : token for authenticating the user
        -> channel_id : id of channel to be removed from
        -> u_id : id of user to be removed
    
    EXCEPTIONS:
    Error type: InputError
        -> Channel ID is not a valid channel
        -> When user with user id u_id is not an owner of the channel
    Error type: AccessError
        -> when the authorised user is not an owner of the flockr,
            or an owner of this channel
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    u_id = int(payload['u_id'])

    return dumps(channel_removeowner(token, channel_id, u_id))

@APP.route("/channels/list", methods=['GET'])
def channels_list_route():
    '''
    DESCRIPTION:
    Provide a list of all channels (and their associated details) that
    the authorised user is part of

    PARAMETERS:
        -> token : token of the usr

    RETURN VALUES:
        -> channels : list of channels

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    token = request.args.get('token')

    return dumps(channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def channels_listall_route():
    '''
    DESCRIPTION:
    Provide a list of all channels (and their associated details)

    PARAMETERS:
        -> token

    RETURN VALUES:
        -> channels : list of channels

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    token = request.args.get('token')

    return dumps(channels_listall(token))

@APP.route("/channels/create", methods=['POST'])
def channels_create_route():
    '''
    DESCRIPTION:
    Creates a new channel with that name that is either a public or
    private channel

    PARAMETERS:
        -> token
        -> name: Name of channel to be created
        -> is_public: Whether the channel is public

    RETURN VALUES:
        -> channel_id : id of the channel created

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
    Error type: InputError
        -> channel name is more than 20 characters long
    '''

    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = bool(payload['is_public'])

    return dumps(channels_create(token, name, is_public))

@APP.route("/message/send", methods=['POST'])
def message_send_route():
    '''
    DESCRIPTION:
    checks that the user if authorised in
    the channel and sends the message

    PARAMETERS:
        -> token
        -> channel_id : id of channel to send message
        -> message : message contents

    RETURN VALUES:
        -> message_id : id of the sent message

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> when the authorised user has not joined the channel they are
           trying to post to
    Error type: InputError
        -> message is more than 1000 characters 
    '''

    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']

    return dumps(message_send(token, channel_id, message))

@APP.route("/message/remove", methods=['DELETE'])
def message_remove_route():
    '''
    DESCRIPTION:
    Given a message_id for a message, this message is removed from the
    channel

    PARAMETERS:
        -> token
        -> message_id : id of the message to be removed

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> message with message_id was sent by the authorised user
           making this request
        -> the authorised user is an owner of this channel or the flockr
    Error type: InputError
        -> message (based on ID) no longer exists
    '''

    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def message_edit_route():
    '''
    DESCRIPTION:
    Given a token, a message_id, and a message,
    finds the sent message with the provided message_id
    and updates its text with the given message.

    PARAMETERS:
        -> token : token of user who called the function
        -> message_id : identification number for intended message to be
        updated
        -> message : updated text

    EXCEPTIONS:
    Error type: AccessError
        -> token passed in is not a valid token
        -> message with message_id was sent by the authorised user
        making this request
        -> the authorised user is an owner of this channel or the flockr
    '''

    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])
    message = payload['message']

    return dumps(message_edit(token, message_id, message))

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
        -> user : information of user

    EXCEPTIONS:
    Error type: InputError
        -> user with u_id is not a valid_user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    u_id = int(request.args.get('u_id'))
    token = request.args.get('token')

    return dumps(user_profile(token, u_id))

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname_route():
    '''
    DESCRIPTION:
    Given a token, replaces the authorised user's first and last name
    with the provided name_first and name_last respectively.

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> name_first : new first name of a user
        -> name_last : new last name of a user
    
    EXCEPTIONS:
    Error type: InputError
        -> name_first is not between 1 and 50 characters inclusively
            in length
        -> name_last is not between 1 and 50 characters inclusively
            in length
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']

    return dumps(user_profile_setname(token, name_first, name_last))

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail_route():
    '''
    DESCRIPTION:
    Updates the authorized user's email address

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> email : new email of a user

    EXCEPTIONS:
    Error type: InputError
        -> email entered is not a valid email
        -> email address is already being used by another user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    payload = request.get_json()
    token = payload['token']
    email = payload['email']

    return dumps(user_profile_setemail(token, email))

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle_route():
    '''
    DESCRIPTION:
    Updates the authorized user's handle (i.e. display name)

    PARAMETERS:
        -> token : token of a user for the particular session (may or
                   may not be authorized)
        -> handle_str : new handle_str of a user

    EXCEPTIONS:
    Error type: InputError
        -> handle_str must be between 3 and 20 characters
        -> handle is already being used by another user
    Error type: AccessError
        -> token passed in is not a valid token
    '''

    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']

    return dumps(user_profile_sethandle(token, handle_str))

@APP.route("/users/all", methods=['GET'])
def users_all_route():
    '''
    DESCRIPTION:
    Returns a list of all users and their associated details

    PARAMETERS:
        -> token : token of a user

    RETURN VALUES:
        -> users : information about all the users

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    token = request.args.get('token')

    return dumps(users_all(token))

@APP.route("/admin/userpermission/change", methods=['POST'])
def change_userpermission_route():
    '''
    DESCRIPTION:
    Given a User by their user ID, set their permissions to
    new permissions described by permission_id

    PARAMETERS:
        -> token : token of user who called invite
        -> u_id : id of the user who is to be invited
        -> permission_id : id of the permission (1 == Owner, 2 == user)

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
         -> when the authorised user is not an owner
    Error type: InputError
    -> u_id does not refer to a valid user
    -> permission_id does not refer to a value permission
    '''

    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])
    permission_id = int(payload['permission_id'])

    return dumps(admin_userpermission_change(token, u_id, permission_id))

@APP.route("/search", methods=['GET'])
def search_route():
    '''
    DESCRIPTION:
    Given a query string, return a collection of messages in
    all of the channels that the user has joined that match the query

    Parameters:
        -> token : token of the invoker
        -> query_str : the target string to search with

    RETURN VALUES:
        -> messages : all messages that contain query_str

    EXCEPTIONS:
    Error type: AccessError
         -> token passed in is not a valid token
    '''

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    return dumps(search(token, query_str))

@APP.route("/clear", methods=['DELETE'])
def clear_route():
    '''
    DESCRIPTION:
    Resets the internal data of the application to it's initial state
    '''

    return dumps(clear())

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

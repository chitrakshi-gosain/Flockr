# Assumptions

- It is assumed that the user enters all the required fields when
  accessing the application

## auth.py
- 1. As of iteration 1, token provided by *auth_register* are not
     unique to the login session.
- 2. Password can be maximum 32 characters long
- 3. Password will only consist of printable ASCII characters

### auth_login
- 1. As of iteration 1, token provided by *auth_login* are not
     unique to the login session.

### auth_logout
- 1. " " is an invalid token

### auth_register
- 1. It logs the user in
- 2. The generated handle can be alphanumeric
- 3. If the generated handle is already taken, a modified handle is
     assigned to the user by adding his u_id at the end of the handle
- 4. u_id is always a positive whole number
- 5. name_first and name_last can have both ASCII and Non-ASCII characters
- 6. name_first and name_last that are purely whitespace are not valid
- 7. User becomes admin of the flockr


## channel.py

### channel_invite
- 1. " " is an invalid token
- 2. User cannot be invited if they are already in the channel -as if function
     was not called
- 3. ids can only be non-negative integers

### channel_details
- 1. An admin can get the details from any channel
- 2. If the channel owner leaves a channel that they created,
and the channel is empty, the channel still exists

### channel_messages
- 1. An admin can get the messages of any channel
- 2. If the channel owner leaves a channel that they created,
the messages still exists.
- 3. If the channel owner leaves a channel that they created,
they cannot read the messages in the channel.

### channel_leave
- 1. " " is an invalid token
- 2. ids can only be non-negative integers

### channel_join
- 1. " " is an invalid token
- 2. User cannot join if they are already in the channel -as if function was
     not called
- 3. ids can only be non-negative integers
- 4. The first user to sign up is a global owner

### channel_addowner
- 1. User with u_id is already a member of channel with channel_id
- 2. -1 is not a valid channel ID
- 3. ' ' is not a valid token

### channel_removeowner
- 1. User with u_id is already a member of channel with channel_id
- 2. -1 is not a valid channel ID
- 3. ' ' is not a valid token

## channels.py

### channels_list
- 1. Channels are listed in order of creation

### channels_listall
- 1. Includes private channels
- 2. Channels are listed in order of creation

### channels_create
- 1. Channel names can be empty strings
- 2. Two channels can share a name
- 3. Channel names can have spaces and special characters
- 4. User who creates a channel becomes an owner and member of that channel

## message.py
### message_send
- 1. If an owner leaves their channel, they cannot send messages to the channel anymore.
- 2. Admins may send any messages in any channel if they are in the channel.

### message_remove
- 1. Admins may remove any messages in any channel.
- 2. If a user leaves their channel, they cannot delete messages from the channel anymore.

### message_edit
- 1. ' ' is not a valid token

### message_react
- 1. ' ' is not a valid token
- 2. 1 is the only valid react ID

### message_unreact
- 1. ' ' is not a valid token
- 2. 1 is the only valid react ID

### message_pin
- 1. Admin can pin messages in any channel if they are in the channel
- 2. If an owner sends a message in a channel and then leaves the channel, they
     cannot pin the message.

### message_unpin
- 1. Admin can unpin messages in any channel if they are in the channel
- 2. If an owner pins a message and then leaves a channel, they cannot unpin the message 
     until the join the channel again.

## user.py

### user_profile_setemail
- 1. If a user tries to update his email-id to what his previous email-id was,
     it is considered a valid email updatation request

### user_profile_sethandle
- 1. Handles can have both ASCII and Non-ASCII characters
- 2. Handles that are purely whitespace are not valid
- 3. If a user tries to update his handle to what his previous handle was, it
     is considered a valid handle updatation request

### user_profile_setname
- 1. ' ' is not a valid token

## other.py

### users_all
- 1. Users displayed in order of registration

### search
- 1. ' ' is an invalid token
- 2. Admins can see all messages
- 3. '' will return all visible messages

### admin_userpermission_change
- 1. There must always be at least 1 global owner

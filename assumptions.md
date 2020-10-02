# Assumptions

## auth.py

### auth_login
- Assumption 1
- etc...

### auth_logout

### auth_register


## channel.py

### channel_invite
- 1. " " is an invalid token
- 2. User cannot be invited if they are already in the channel -as if function was not called
- 3. ids can only be non-negative integers

### channel_details

### channel_messages

### channel_leave
- 1. " " is an invalid token
- 2. ids can only be non-negative integers

### channel_join
- 1. " " is an invalid token
- 2. User cannot join if they are already in the channel -as if function was not called
- 3. ids can only be non-negative integers
- 4. The first user to sign up is a global owner

### channel_addowner

### channel_removeowner


## channels.py

### channels_list
- Channels are listed in order of creation

### channels_listall
- Includes private channels
- Channels are listed in order of creation

### channels_create
- Channel names can be empty strings
- Two channels can share a name
- Channel names can have spaces and special characters
- User who creates a channel becomes an owner and member of that channel
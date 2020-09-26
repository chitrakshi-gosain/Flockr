# Assumptions

## auth.py

### auth_login
- Assumption 1
- etc...

### auth_logout

### auth_register


## channel.py

### channel_invite

### channel_details

### channel_messages

### channel_leave

### channel_join

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
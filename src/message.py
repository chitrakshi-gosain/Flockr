# checks that the user if authorised in the channel and sends the message
def message_send(token, channel_id, message):
    return {
        'message_id': 1,
    }

# checks that the user if authorised in the channel and deletes the message
def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
'''
Created collaboratively by Wed15GrapeTeam2 2020 T3
Contributor - YOUR NAME HERE

Iteration 2
'''

import requests
# from flask_mail import Mail
# from server import APP
# import data

'''
****************************BASIC TEMPLATE******************************
'''

'''
APP.routes_USED_fOR_THIS_TEST("/rule", methods=['METHOD']) return
json.dumps({RETURN VALUE})
-> APP.route("/auth/register", methods=['POST']) return
   json.dumps({u_id, token})
-> APP.route("/auth/passwordreset/request", methods=['POST']) return
   json.dumps({})
'''

'''
FIXTURES_USED_FOR_THIS_TEST (available in src/http_tests/conftest.py)
-> url
-> reset
-> ...
'''

'''
EXCEPTIONS
Error type: InputError
    -> ..
Error type: AccessError
    -> ..
'''

#JUST TRY RECORDING MESSAGES GETTING RESET CODE, EVEN IF IT SENDS THE EMAIL, ITS OK - MICHAEL 9/11/200

# APP.config['MAIL_SUPPRESS_SEND'] = True
# mail = Mail(APP)
# does not stop sending emails

# APP.testing = True
# does not stop sending emails

# APP.config['TESTING'] = True
# mail = Mail(APP)
# technically i should reinstate the mail object, but i'm not passing
# the mail object as an argument so how do i do it? this will still send email :(
# email is still being sent after reinstating the mail object

# TESTING = True
# this does not stop sending emails

def test_url(url):
    '''
    A simple sanity test to check that the server is set up properly
    '''
    assert url.startswith("http")

def test_invalid_email(url, reset):
    '''
    Tests that App.route("/auth/passwordreset/request", methods=['POST'])
    raises an InputError when an invalid email-id is passed as one of
    the parameters
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user0_email.com'
    })

    assert resetrequest_response.status_code == 400

def test_unregistered_user(url, reset):
    '''
    Tests that App.route("/auth/passwordreset/request", methods=['POST'])
    raises an InputError when an unregistered user tries to request for
    a reset code to change his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'user00@email.com'
    })

    assert resetrequest_response.status_code == 400

def test_reset_code_sent_successfully(url, initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully send an email to
    the user with reset code so that he can reset his password
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'chitrakshi6072@gmail.com'
    })

    assert resetrequest_response.status_code == 200

def test_return_type(url, initialise_user_data):
    '''
    Tests that auth_passwordreset_request successfully returns the reset
    code which is of string type as per the spec
    '''

    resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'chitrakshi6072@gmail.com'
    })
    assert resetrequest_response.status_code == 200
    resetrequest_payload = resetrequest_response.json()

    assert not resetrequest_payload

# THIS IS MEANT TO BE A SANITY CHECK WHITEBOX TO CONFIRM MESSAGES WERE RECORDED PROPERLY, DOESN'T WORK ATM
# def test_trying_to_record_emails(url, initialise_user_data):
#     with mail.record_messages() as outbox:
#         resetrequest_response = requests.post(f"{url}/auth/passwordreset/request", json={
#             'email': 'chitrakshi6072@gmail.com'
#         })
#         assert resetrequest_response.status_code == 200
#         assert len(outbox) == 1
#         assert outbox[0].body == data.data['password_record']['chitrakshi6072@gmail.com']

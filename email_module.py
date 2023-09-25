from flask import Flask, redirect, session, url_for
from flask_oauthlib.client import OAuth
import base64
from Crypto.Cipher import AES
import os

app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Change this in production to a secure secret key
oauth = OAuth(app)

# Encryption-related functions
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def encrypt(raw, key):
    raw = pad(raw)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, key):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc[AES.block_size:]).rstrip(b"\0")

# Google OAuth setup
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/gmail.readonly'
    },
    base_url='https://www.googleapis.com/gmail/v1/users/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Yahoo and Outlook OAuth setups would be similar...
# yahoo = oauth.remote_app( ... )
# outlook = oauth.remote_app( ... )

@app.route('/login_google')
def login_google():
    return google.authorize(callback=url_for('authorized_google', _external=True))

@app.route('/login_callback_google')
def authorized_google():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    # Encrypt the token before storing
    encrypted_token = encrypt(response['access_token'], app.secret_key)  # This is a simple way; consider enhancing security further
    # Store encrypted_token in database or other safe storage
    
    return 'Logged in successfully!'

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# Implement similar routes and token getters for Yahoo and Outlook

# TLS Configuration
if __name__ == '__main__':
    app.run(ssl_context=('path_to_cert.pem', 'path_to_key.pem'))

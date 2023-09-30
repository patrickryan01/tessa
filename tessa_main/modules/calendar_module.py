from flask import Flask, redirect, session, url_for, jsonify, request
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

# Google Calendar OAuth
google_calendar = oauth.remote_app(
    'google_calendar',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/calendar'
    },
    base_url='https://www.googleapis.com/calendar/v3/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Routes
@app.route('/login_google_calendar')
def login_google_calendar():
    return google_calendar.authorize(callback=url_for('authorized_google_calendar', _external=True))

@app.route('/login_callback_google_calendar')
def authorized_google_calendar():
    response = google_calendar.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied!'
    
    session['google_token'] = (response['access_token'], '')
    me = google_calendar.get('users/me')
    return jsonify({"data": me.data})

@app.route('/google_fetch_events')
def google_fetch_events():
    response = google_calendar.get('calendars/primary/events')
    return jsonify(response.data)

@app.route('/google_add_event', methods=['POST'])
def google_add_event():
    data = request.json
    response = google_calendar.post('calendars/primary/events', data=data)
    return jsonify(response.data)

@app.route('/google_update_event/<event_id>', methods=['POST'])
def google_update_event(event_id):
    data = request.json
    response = google_calendar.put(f'calendars/primary/events/{event_id}', data=data)
    return jsonify(response.data)

@app.route('/google_delete_event/<event_id>', methods=['DELETE'])
def google_delete_event(event_id):
    response = google_calendar.delete(f'calendars/primary/events/{event_id}')
    return jsonify(response.data)

# Token Getter
@google_calendar.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# TLS Configuration
if __name__ == '__main__':
    app.run(ssl_context=('path_to_cert.pem', 'path_to_key.pem'))

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

Base = declarative_base()

DATABASE_URL = "sqlite:///./test.db"  # Modify for your actual database

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    encrypted_data = Column(String(500))

    def __init__(self, username, data, key):
        self.username = username
        self.encrypted_data = self.encrypt_data(data, key)

    def encrypt_data(self, data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        encrypted = nonce + ciphertext
        return encrypted.hex()

    def decrypt_data(self, key):
        encrypted = bytes.fromhex(self.encrypted_data)
        nonce = encrypted[:16]
        ciphertext = encrypted[16:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode()


Base.metadata.create_all(engine)


def create_user(username, data, key):
    session = Session()
    new_user = User(username, data, key)
    session.add(new_user)
    session.commit()
    session.close()


def get_user_data(username, key):
    session = Session()
    fetched_user = session.query(User).filter_by(username=username).first()
    session.close()
    if fetched_user:
        return fetched_user.decrypt_data(key)
    else:
        return None

# For Flask integration and setting up TLS
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def add_user():
    username = request.json.get('username')
    data = request.json.get('data')
    key = request.json.get('key')  # IMPORTANT: Do not send the key like this in real-world scenarios
    create_user(username, data, key)
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    key = request.args.get('key')  # IMPORTANT: Do not send the key like this in real-world scenarios
    data = get_user_data(username, key)
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(ssl_context=('path_to_cert.pem', 'path_to_key.pem'))
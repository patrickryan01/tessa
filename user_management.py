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



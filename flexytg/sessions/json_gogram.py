import os
import base64
import json
import struct
import binascii
import hashlib
from Crypto.Cipher import AES

# the default aes key
# aes_key = b"1234567890123456"

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    return data[:-data[-1]]

def unjson_gogram(session_file=None,aes_key=b"1234567890123456"):
    if session_file is None:
        raise ValueError('Session File Is Missing')
    with open(session_file, "rb") as f:
        raw = f.read()
    data = json.loads(unpad(AES.new(aes_key, AES.MODE_ECB).decrypt(raw)).decode())
    dict_data = {
        "key": base64.b64decode(data["key"]),
        "hash": base64.b64decode(data["hash"]),
        "salt": struct.unpack('<Q', base64.b64decode(data["salt"]))[0],
        "hostname": data["hostname"],
        "app_id": data["app_id"]
    }
    return dict_data

def json_gogram(file_name='gogram.json', auth_key=None,auth_key_hash=None,salt=None,hostname='149.154.167.91',app_id=None,aes_key=b"1234567890123456"):
    if file_name is None:
        file_name = 'gogram.json'
    file_name = str(file_name) if str(file_name).endswith('.json') else str(file_name) + '.json'
    if app_id and auth_key:
        if len(auth_key) == 256:
           auth_key = auth_key
        else:   
           try:
              auth_key = base64.b64decode(auth_key)
           except binascii.Error:
              raise ValueError('Auth Key Invalid Or Not In Supported Types (Raw Bytes, Base64)')
        if auth_key_hash:
            auth_key_hash = auth_key_hash
        else:
            auth_key_hash = (hashlib.sha1(auth_key).digest())[12:20]
        session_data = {
        "key": base64.b64encode(auth_key).decode(),
        "hash": base64.b64encode(auth_key_hash).decode(),
        "salt": base64.b64encode(struct.pack('<Q', salt)).decode(),
        "hostname": hostname,
        "app_id": app_id
    }
        session = AES.new(aes_key, AES.MODE_ECB).encrypt(pad(json.dumps(session_data).encode()))
        with open(file_name, "wb") as f:
            f.write(session)

import base64
import struct
import hashlib
import binascii
import time

SESSION_PREFIX = "1BvX"

def string_gogram(auth_key=None, auth_key_hash=None, dc_id=None, ip_addr='149.154.167.91', app_id=None):
    if auth_key and dc_id and app_id:
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
        
        session_contents = [
            auth_key.decode(),
            auth_key_hash.decode(),
            ip_addr,
            str(dc_id),
            str(app_id)
            ]
        combined = "::".join(session_contents)
        encoded = base64.urlsafe_b64encode(combined.encode()).decode().rstrip("=")
        session_string = SESSION_PREFIX + encoded
        dict_data = {
            'session_string': session_string,
            'time': int(time.time())
        }

def unstring_gogram(string_session=None):
    if string_session is None:
        raise ValueError("Session string not provided")
    if not string_session.startswith(SESSION_PREFIX):
        raise ValueError("Invalid session string")

    string_data = string_session[4:]
    session_data = base64.urlsafe_b64decode(string_data + "==").decode()
    parts = session_data.split("::")
    
    if len(parts) != 5:
        raise ValueError("The session string is invalid or has been tampered with")

    auth_key = parts[0].encode()
    auth_key_hash = parts[1].encode()
    ip_addr = parts[2]
    dc_id = int(parts[3])
    app_id = int(parts[4])

    dict_data = {
        "auth_key": auth_key,
        "auth_key_hash": auth_key_hash,
        "dc_id": dc_id,
        "ip_addr": ip_addr,
        "app_id": app_id
    }
    return dict_data

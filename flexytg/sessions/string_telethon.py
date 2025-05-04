#Function To Pack And Unpack Telethon String Sessions

#Imports
import base64
import struct
import time
import socket
import binascii

#Vars
CURRENT_VERSION = '1'
_STRUCT_PREFORMAT = '>B{}sH256s'

#Defs
def string_telethon(dc_id=None,server_address='149.154.167.91',port=443,auth_key=None):
    if dc_id and auth_key:
        try:
           info = socket.getaddrinfo(server_address, None)
           if info:
              family = info[0][0]
              if family == socket.AF_INET:
                 ip = socket.inet_pton(socket.AF_INET, server_address)
              elif family == socket.AF_INET6:
                 ip = socket.inet_pton(socket.AF_INET6, server_address)
              else:
                 raise ValueError('Only IPv4 and IPv6 are supported in this format')
        except socket.gaierror as e:
           raise Exception(f"Socket error occurred: {e}")
        if len(auth_key) == 256:
           auth_key = auth_key
        else:   
           try:
              auth_key = base64.b64decode(auth_key)
           except binascii.Error:
              raise ValueError('Auth Key Invalid Or Not In Supported Types (Raw Bytes, Base64)')
        raw = struct.pack('>B4sH256s', dc_id, ip, port, auth_key)
        dict_data = {
            'string_session': CURRENT_VERSION + base64.urlsafe_b64encode(raw).decode('ascii'),
            'time': int(time.time())
        }
        return dict_data
    else:
        raise ValueError('Nor DC ID or Auth Key Have Been Provided')
    
def unstring_telethon(string_session=None):
    if string_session:
       if string_session[0] != CURRENT_VERSION:
          raise ValueError('Not a valid string')
       string_session = string_session[1:]
       ip_len = 4 if len(string_session) == 352 else 16
       dc_id, server_adress, port, auth_key = struct.unpack(
                _STRUCT_PREFORMAT.format(ip_len), base64.urlsafe_b64decode(string_session) if str(type(string_session)) == "<class 'bytes'>" else base64.urlsafe_b64decode(string_session.encode()))
       dict_data = {
            'dc_id': dc_id,
            'server_adress': server_adress,
            'date': time.time(),
            'port': port,
            'auth_key': auth_key
            }
       return dict_data
    else:
       raise ValueError("Session string not provided")

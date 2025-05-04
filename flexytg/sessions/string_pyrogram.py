#Function To Pack And Unpack Pyrogram String Sessions

#Imports
import base64
import struct
import time
import binascii

#Vars
SESSION_STRING_FORMAT = ">BI?256sQ?"

#Defs
def string_pyrogram(dc_id=None,api_id=None,test_mode=0,auth_key=None,date=int(time.time()),user_id=None,is_bot=0):
    if dc_id and api_id and auth_key and user_id:
        if len(auth_key) == 256:
           auth_key = auth_key
        else:   
           try:
              auth_key = base64.b64decode(auth_key)
           except binascii.Error:
              raise ValueError('Auth Key Invalid Or Not In Supported Types (Raw Bytes, Base64)')
        packed = struct.pack(
                SESSION_STRING_FORMAT,
                dc_id,
                api_id,
                test_mode,
                auth_key,
                user_id,
                is_bot
            )
        dict_data = {
            'string_session': base64.urlsafe_b64encode(packed).decode().rstrip("="),
            'time': int(time.time())
        }
        return dict_data
    else:
        raise Exception('Nor DC ID or Auth Key Or Api Id Or User ID Have Been Provided')

def unstring_pyrogram(string_session=None):
    if string_session:
       dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                SESSION_STRING_FORMAT,
                base64.urlsafe_b64decode(string_session + "=" * (-len(string_session) % 4)))
       dict_data = {
                    'dc_id': dc_id,
                    'api_id': api_id,
                    'test_mode': test_mode,
                    'auth_key': auth_key,
                    'user_id': user_id,
                    'is_bot': is_bot
                    }
       return dict_data
    else:
      raise ValueError('Session String Not Provided')

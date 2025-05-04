from .string_pyrogram import string_pyrogram
from .string_hydrogram import string_hydrogram
from .string_telethon import string_telethon
from .sql_telethon import sql_telethon
from .sql_hydrogram import sql_pyrogram
from .sql_pyrogram import sql_hydrogram
from .json_gogram import json_gogram
from .string_gogram import string_gogram
def create_session(module_name=None,session_type=None,file_name=None,dc_id=None,api_id=None,test_mode=0,date=None,user_id=None,is_bot=0,server_address='149.154.167.91',port=443,auth_key=None,entities_file=None):
    if module_name == 'telethon':
       if session_type == 'string':
          return string_telethon(dc_id=dc_id,server_address=server_address,port=port,auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'))
       elif session_type == 'sql':
          return sql_telethon(file_name=file_name, dc_id=dc_id, server_address=server_address, port=port, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'))
    elif module_name == 'pyrogram':
       if session_type == 'string':
          return string_pyrogram(dc_id=dc_id, api_id=api_id, test_mode=test_mode, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'),date=date, user_id=user_id, is_bot=is_bot)
       elif session_type == 'sql':
           return sql_pyrogram(file_name=file_name, dc_id=dc_id, api_id=api_id, test_mode=test_mode, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'),date=date, user_id=user_id, is_bot=is_bot)
     elif module_name == 'hydrogram':
       if session_type == 'string':
          return string_hydrogram(dc_id=dc_id, api_id=api_id, test_mode=test_mode, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'),date=date, user_id=user_id, is_bot=is_bot)
       elif session_type == 'sql':
           return sql_hydrogram(file_name=file_name, dc_id=dc_id, api_id=api_id, test_mode=test_mode, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'),date=date, user_id=user_id, is_bot=is_bot)
    elif module_name == 'gogram':
       if session_type == 'string':
           return string_gogram(dc_id=dc_id, app_id=api_id, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'))
       elif session_type == 'json':
           return json_gogram(file_name=file_name, dc_id=dc_id, app_id=api_id, auth_key=auth_key if str(type(auth_key)) == "<class 'bytes'>" else auth_key.encode('utf-8'),date=date, user_id=user_id, is_bot=is_bot)
    else:
       print('Unsupported Type')

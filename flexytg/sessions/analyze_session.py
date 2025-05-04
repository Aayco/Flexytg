from .string_pyrogram import unstring_pyrogram
from .string_hydrogram import unstring_hydrogram
from .string_telethon import unstring_telethon
from .sql_telethon import unsql_telethon
from .sql_pyrogram import unsql_pyrogram
from .sql_hydrogram import unsql_hydrogram
from .json_gogram import unjson_gogram
from .string_gogram import unstring_gogram
def analyze_session(module_name=None,session_type=None,string_session=None,sql_session=None,json_session=None,aes_key=None):
    if module_name == 'telethon':
       if session_type == 'string':
          if string_session:
             return unstring_telethon(string_session=string_session)
       elif session_type == 'sql':
          if sql_session:
             return unsql_telethon(sql_session=sql_session)
    elif module_name == 'pyrogram':
       if session_type == 'string':
          if string_session:
             return unstring_pyrogram(string_session=string_session)
       elif session_type == 'sql':
           return unsql_pyrogram(sql_session=sql_session)
     elif module_name == 'pyrogram':
       if session_type == 'string':
          if string_session:
             return unstring_hydrogram(string_session=string_session)
       elif session_type == 'sql':
           return unsql_hydrogram(sql_session=sql_session)
    elif module_name == 'gogram':
       if session_type == 'string':
          if string_session:
             return unstring_gogram(string_session=string_session)
       elif session_type == 'json':
           return unjson_gogram(sql_session=sql_session)
    else:
       print('Unsupported Type')

#Function To Pack And Unpack Pyrogram Sql Sessions

#Imports
import sqlite3
import base64
import json
import binascii
import time

#Vars
entities = []

VERSION = 3

SCHEMA = '''
CREATE TABLE IF NOT EXISTS sessions (
    dc_id INTEGER NOT NULL,
    api_id INTEGER NOT NULL,
    test_mode INTEGER DEFAULT 0,
    auth_key BLOB NOT NULL,
    date INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_bot INTEGER DEFAULT 0,
    PRIMARY KEY (dc_id, user_id)
);

CREATE TABLE IF NOT EXISTS version (
    version INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS peers (
    id INTEGER NOT NULL,
    access_hash BLOB NOT NULL,
    type TEXT NOT NULL,
    username TEXT,
    phone_number TEXT,
    last_update_on INTEGER,
    PRIMARY KEY (id)
);
'''

#Defs
def unsql_pyrogram(sql_session=None):
    if sql_session is None:
        return
    conn = sqlite3.connect(sql_session)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT dc_id, api_id, test_mode, auth_key, date, user_id, is_bot FROM sessions LIMIT 1")
        dc_id, api_id, test_mode, auth_key, date, user_id, is_bot = cursor.fetchone()
        cursor.execute("SELECT id, access_hash, type, username, phone_number, last_update_on FROM peers")
        results = cursor.fetchall()
        for id, access_hash, type, username, phone_number, last_update_on in results:
            data = {
                'id':id,
                'access_hash':access_hash,
                'type': type,
                'username':username,
                'phone_number': phone_number,
                'last_update_on': last_update_on,
                }
            entities.append(data)
    except sqlite3.OperationalError:
        raise Exception('Session Is Invaild')
    dict_data = {
        'dc_id': dc_id,
        'api_id': api_id,
        'test_mode': test_mode,
        'auth_key': __import__('base64').b64encode(auth_key).decode(),
        'date': date,
        'user_id': user_id,
        'is_bot': is_bot,
        'entities': entities
    }
    return dict_data

def sql_pyrogram(file_name='pyrogram.session', dc_id=None, api_id=None, test_mode=0, auth_key=None, 
                 date=None, user_id=None, is_bot=0, last_update_on=None, entities_file=None):
    date = date or int(time.time())
    last_update_on = last_update_on or date

    if file_name is None:
        file_name = 'pyrogram.session'
    file_name = str(file_name) if str(file_name).endswith('.session') else str(file_name) + '.session'

    if dc_id and api_id and auth_key and user_id: 
        if len(auth_key) == 256:
            auth_key = auth_key
        else:
            try:
                auth_key = base64.b64decode(auth_key)
            except binascii.Error:
                raise ValueError('Auth Key Invalid Or Not In Supported Types (Raw Bytes, Base64)')
    else:
        raise Exception('No DC ID, Auth Key, API ID, or User ID Provided')

    conn = sqlite3.connect(file_name)
    conn.executescript(SCHEMA)
    conn.execute("INSERT INTO version VALUES (?)", (VERSION,))
    conn.execute(
        "INSERT INTO sessions (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot)
    )

    if entities_file:
        with open(entities_file, 'r') as f:
            entities = json.load(f)
            for entity in entities:
                conn.executemany(
                    "REPLACE INTO peers (id, access_hash, type, username, phone_number, last_update_on) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [(entity['id'], entity['access_hash'], entity['type'], entity['username'],
                      entity['phone_number'], entity.get('last_update_on', last_update_on)) for entity in entities]
                )

    conn.commit()
    conn.close()

    return f'Session {file_name} Created Successfully :3'

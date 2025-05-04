#Function To Pack And Unpack Telethon Sql Sessions

#Imports
import sqlite3
import base64
import time
import json
import binascii

#Vars
entities = []

#Defs
def unsql_telethon(sql_session=None):
    if sql_session is None:
        return
    conn = sqlite3.connect(sql_session)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT dc_id, server_address, port, auth_key FROM sessions LIMIT 1")
        dc_id, server_address, port, auth_key = cursor.fetchone()
        cursor.execute("SELECT id, hash, username, phone, name, date FROM entities")
        results = cursor.fetchall()
        for id,hash,username,phone,name,date in results:
            data = {
                'id':id,
                'hash':hash,
                'username':username,
                'phone': phone,
                'name': name,
                'date': date,
                'type': 'user' if id > 0 else 'chat',
                }
            entities.append(data)
    except sqlite3.OperationalError:
        raise Exception('Session Is Invaild')
    dict_data = {
            'dc_id': dc_id,
            'server_adress': server_address,
            'date': time.time(),
            'port': port,
            'auth_key': __import__('base64').b64encode(auth_key).decode(),
            'entities': entities
            }
    return dict_data

def sql_telethon(file_name='telethon.session', dc_id=None, server_address='149.154.167.91', port=443, auth_key=None, takeout_id=None, entities_file=None):
    if file_name is None:
        file_name = 'telethon.session'
    file_name = str(file_name) if str(file_name).endswith('.session') else str(file_name) + '.session'
    conn = sqlite3.connect(file_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS version (
        version INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY,
        hash INTEGER,
        username TEXT,
        phone TEXT,
        name TEXT,
        date INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sent_files (
    md5_digest BLOB,
    file_size INTEGER,
    type INTEGER,
    id INTEGER,
    hash INTEGER,
    PRIMARY KEY(md5_digest, file_size, type)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
    dc_id INTEGER PRIMARY KEY,
    server_address TEXT,
    port INTEGER,
    auth_key BLOB,
    takeout_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS update_state (
    id INTEGER PRIMARY KEY,
    pts INTEGER,
    qts INTEGER,
    date INTEGER,
    seq INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS android_metadata (
        locale TEXT
    )
    """)

    cursor.execute("INSERT INTO version (version) VALUES (?)", (7,))

    if dc_id and auth_key:
        if len(auth_key) == 256:
           auth_key = auth_key
        else:   
           try:
             auth_key = base64.b64decode(auth_key)
           except binascii.Error:
             raise ValueError('Auth Key Invalid Or Not In Supported Types (Raw Bytes, Base64)')
        cursor.execute("INSERT OR REPLACE INTO sessions (dc_id, server_address, port, auth_key, takeout_id) VALUES (?, ?, ?, ?, ?)",
                   (dc_id, server_address, port, auth_key, takeout_id))
    else:
        exit('You Have To Provide DC ID And Auth Key')
        os.remove(file_name)
    
    cursor.execute("INSERT OR REPLACE INTO version (version) VALUES (?)", (7,))
    
    cursor.execute("INSERT OR REPLACE INTO android_metadata (locale) VALUES (?)", ('en_US',))

    if entities_file:
        with open(entities_file, 'r') as f:
            entities = json.load(f)
            for entity in entities:
                cursor.execute("INSERT OR REPLACE INTO entities (id, hash, username, phone, name, date) VALUES (?, ?, ?, ?, ?, ?)",
                       (entity['id'], entity['hash'], entity['username'], entity['phone'], entity['name'], entity['date']))

    conn.commit()
    conn.close()
    return f'Session {file_name} Created Successfully :3'

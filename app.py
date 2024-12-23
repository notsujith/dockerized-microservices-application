import base64
import hashlib
import hmac
import sqlite3
import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)
db_name = "logs.db"
sql_file = "logs.sql"
db_flag = False


def create_db():
    global db_flag
    conn = sqlite3.connect(db_name)
    with open(sql_file, 'r') as sql_startup:
        init_db = sql_startup.read()

    cursor = conn.cursor()
    cursor.executescript(init_db)
    conn.commit()
    conn.close()
    db_flag = True
    return conn


def get_db():
    if not db_flag:
        create_db()
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def init_db():
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        with open(sql_file, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    return "Initialized"


@app.route('/clear', methods=(['GET']))
def clear():
    os.remove(db_name) if os.path.exists(db_name) else None
    db_flag = False
    init_db()
    return "Cleared"


@app.route('/log_event', methods=['POST'])
def log_event():
    event = request.form.get('event')
    user = request.form.get('user')
    filename = request.form.get('filename')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (event, user, filename) VALUES (?, ?, ?);', (event, user, filename))
    conn.commit()
    conn.close()
    return json.dumps({'status': 1})


@app.route('/view_log', methods=['GET'])
def view_log():
    jwt = request.headers.get('Authorization')
    LOGINURL = f"http://users:5000/check_login/{jwt}"
    r = requests.get(url=LOGINURL)
    login_data = r.json()
    if login_data['status'] != 1:
        return json.dumps({'status': 2, 'data': 'NULL'})

    encoded_header, encoded_payload, signature = jwt.split('.')
    decoded_payload = base64.urlsafe_b64decode(encoded_payload + '==')
    payload = json.loads(decoded_payload.decode('utf-8'))
    requesting_user = payload['username']

    username = request.args.get('username')
    filename = request.args.get('filename')

    if username:
        if username != requesting_user:
            return json.dumps({'status': 3, 'data': 'NULL'})
        query = "SELECT event, user, filename FROM logs WHERE user = ? ORDER BY created;"
        params = (username,)
    elif filename:
        DOCURL = f"http://documents:5001/get_document/{filename}"
        r = requests.get(url=DOCURL)
        doc_data = r.json()
        if 'status' not in doc_data or doc_data['status'] != 1:
            return json.dumps({'status': 3, 'data': 'NULL'})

        USERURL = f"http://users:5000/get_user/{requesting_user}"
        r = requests.get(url=USERURL)
        user_data = r.json()
        if 'status' not in user_data or user_data['status'] != 1:
            return json.dumps({'status': 3, 'data': 'NULL'})

        user_group = user_data['group']
        doc_groups = json.loads(doc_data['data']['groups'])
        if user_group not in doc_groups.values():
            return json.dumps({'status': 3, 'data': 'NULL'})
        query = "SELECT event, user, filename FROM logs WHERE filename = ? ORDER BY created;"
        params = (filename,)
    else:
        return json.dumps({'status': 2, 'data': 'NULL'})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()

    data = {}
    for idx, log in enumerate(logs, start=1):
        event, user, filename = log
        if filename is None:
            filename = 'NULL'
        data[str(idx)] = {
            'event': event,
            'user': user,
            'filename': filename
        }

    return json.dumps({'status': 1, 'data': data})
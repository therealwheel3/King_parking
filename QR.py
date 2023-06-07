import random
import sqlite3
import time
import qrcode
from random import choice

db = sqlite3.connect("database.db", check_same_thread=False)
def create_qr(parking_id, server):
    abc = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    cur = db.cursor()
    place = choice(cur.execute(f'''SELECT name FROM 'place_data_base' WHERE ocupied == 0 AND parking == {parking_id}''').fetchall())
    cur.execute(f'''UPDATE place_data_base SET `ocupied` = '1' WHERE `name` = '{place[0]}'
                ''')
    code = ''.join([abc[random.randint(0, len(abc) - 1)] if i % 5 != 0 else '-' for i in range(1, 20)]) + f'-{parking_id}'
    place = place[0]
    cur.execute(f'''INSERT INTO 'token_data_base'('parking', 'place', 'start', 'end', 'token', 'condition')
        VALUES(
        '{parking_id}', '{place}', '{time.time()}', '{time.time() + 86400}', '{code}', '0'
        )''')
    db.commit()
    QR = qrcode.make(f'{server}/check/{code}')
    QR.save(f'static/QR/{code}.png')
    return (code, QR)


host = '127.0.0.1'
port = 8080
server = f'{host}:{port}'
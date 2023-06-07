import sqlite3
from werkzeug.security import (check_password_hash, generate_password_hash)
import time

db = sqlite3.connect("database.db", check_same_thread=False)


def OWNER_reg(email_adress, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    res = cur.execute(
        f'''
            SELECT `email_adress` FROM `OWNER_data_base` WHERE `email_adress` = '{email_adress}'
        '''
    ).fetchall()
    db.commit()
    if len(res) == 0:
        cur.execute(
            f'''
                INSERT INTO `OWNER_data_base`(`email_adress`, `password`, 'created_at', 'updated_at')
                VALUES (
                    '{email_adress}',
                    '{generate_password_hash(psw)}',
                    {time.time()}, {time.time()}
                )
            '''
        )
        db.commit()
        return {
            "msg": "Вы успешно зарегистрировались!",
            "status": True,
            "id": get_OWNER_id(email_adress)["id"]
        }
    return {
        "msg": "Такой e-mail уже зарегистрирован!",
        "status": False
    }

def get_OWNER_id(email_adress):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id` FROM `OWNER_data_base` WHERE `email_adress` = '{email_adress}'
        '''
    )
    res = cur.fetchall()
    db.commit()
    return {
        "id": res[0]["id"]
    }

def OWNER_log(email_adress, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `email_adress`, `password` FROM `OWNER_data_base`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row['email_adress'] == email_adress and check_password_hash(
            row['password'],
            psw
        ) or row['email_adress'] == email_adress and psw == row['password']:
            return {
                "msg": "Вы успешно вошли",
                "status": True,
                "id": row["id"]
            }
    else:
        return {
            "msg": "Неверный логин/пароль!",
            "status": False
        }

def owner_check_psw(user_id, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `password` FROM `OWNER_data_base`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["id"] == int(user_id) and check_password_hash(
            row["password"],
            psw
        ):
            return {
                "msg": "Пароли совпали",
                "status": True,
            }
    else:
        return {
            "msg": "Пароли не совпали",
            "status": False
        }
    
def add_PARKING(name, adress, cost, count_places):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    length = len(cur.execute('''SELECT 'id' from parking_data_base''').fetchall())
    cur.execute(
        f'''
            INSERT OR IGNORE INTO `parking_data_base`(`id`, `name`, 'adress', 'cost')
            VALUES (
                '{length + 1}', '{name}', '{adress}', '{cost}'
            )
        '''
    )
    for i in range(1, count_places + 1):
        add_PLACES(i, length + 1)
    db.commit()

def add_PLACES(name, park):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    length = len(cur.execute('''SELECT 'id' from place_data_base''').fetchall())
    cur.execute(f'''
        INSERT OR IGNORE INTO place_data_base('id', 'name', 'parking', 'ocupied')
        VALUES('{length + 1}', '{name}', '{park}', '0')
    ''')
    db.commit()

def check_TOKEN(token):
    cur = db.cursor()
    token_list = cur.execute('''
        SELECT token FROM 'token_data_base' 
        ''').fetchall()
    token_list = list(map(lambda x: x[0], token_list))
    if token in token_list:
        return True
    return False
    
def return_PARKINGS():
    cur = db.cursor()
    response = cur.execute('''SELECT * FROM parking_data_base''').fetchall()
    return response

def return_PARKINGS_id(id_):
    cur = db.cursor()
    response = cur.execute(f'''SELECT * FROM parking_data_base WHERE `id` = '{id_}'
                           ''').fetchall()
    return response

def return_place_count(id_):
    cur = db.cursor()
    response = cur.execute(f'''SELECT * FROM place_data_base WHERE `Parking` = '{id_}'
                           ''').fetchall()
    return len(response)

def return_free_places(id_):
    cur = db.cursor()
    response = cur.execute(f'''SELECT * FROM place_data_base WHERE `Parking` = '{id_}' AND `ocupied` = '0'
                           ''').fetchall()
    return any(response)
    
def get_place_condition(token):
    cur = db.cursor()
    res = cur.execute(f'''SELECT condition FROM token_data_base WHERE `token` = '{token}'
                      ''').fetchall()
    return res[0][0]

def edit_token_condition(token):
    cur = db.cursor()
    con = cur.execute(f'''SELECT condition FROM token_data_base WHERE token = '{token}'
                      ''').fetchall()
    if con[0][0] == '0':
        cur.execute(f'''UPDATE token_data_base SET condition = '1' WHERE token = '{token}'
                ''')
    else:
        pass
    db.commit()

def delete_token(token):
    cur = db.cursor()
    res = cur.execute(f'''SELECT place FROM token_data_base WHERE `token` = '{token}'
                      ''').fetchall()[0][0]
    cur.execute(f'''DELETE from token_data_base WHERE `token` = '{token}'
                ''')
    db.commit()
    cur.execute(f'''UPDATE place_data_base SET ocupied = '0' WHERE name = '{res}'
                ''')
    db.commit()
    
def return_parking_info(token):
    cur = db.cursor()
    res = cur.execute(f'''SELECT `name`, `adress` FROM parking_data_base WHERE
                      id = (SELECT parking FROM token_data_base WHERE token = '{token}')''').fetchall()[0]
    return res



if __name__ == '__main__':
    delete_token('9hth-k4ch-y18s-08jq-1')
    pass
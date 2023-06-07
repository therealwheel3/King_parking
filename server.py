from flask import Flask, render_template, request, session
import connection
import sqlite3
from flask import redirect
from QR import create_qr
import email_validate


app = Flask(__name__)
app.config['SECRET_KEY'] = '8hfer^swutu*sd8uwtrg$w83u4&t8-u9'
db = sqlite3.connect("database.db", check_same_thread=False)
host = '127.0.0.1'
port = 8080
server = f'{host}:{port}'
logo = 'static/logo.svg'
owners = 'static/owners.svg'
arrow = 'static/arrow.svg'
style = 'static/style.css'
bg = 'static/lk-bg.png'
script = 'static/script.js'
validation = 'static/validation.js'
add_parking = 'static/add-parking.js'


@app.route('/')
def index():
    return render_template('index.html', 
                            logo=logo, owners=owners, arrow=arrow, style=style,
                            bg=bg, script=script, validation=validation)

@app.route('/check/<token>')
def check_token(token):
    if connection.check_TOKEN(token):
        if connection.get_place_condition(token) == '0':
            connection.edit_token_condition(token)
            res = connection.return_parking_info(token)
            return f'<h1>ТОКЕН ВАЛИДЕН</h1>\n<h2>Название парковки: {res[0]}</h2>\n<h2>Адрес парковки: {res[-1]}</h2>'
        else:
            connection.delete_token(token)
            return '<h1>ТОКЕН ИСПОЛЬЗОВАН</h1>'
    return '<h1>ТОКЕН НЕ ВАЛИДЕН</h1>'

@app.route('/owner_login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    if connection.OWNER_log(login, password)['status']:
        session['is_log'] = True
        return redirect('/success')
    return render_template('sign-in.html', title='Авторизация', logo=logo, 
                           owners=owners, arrow=arrow, style=style,
                            bg=bg, script=script, validation=validation)

@app.route('/owner_reg', methods=['GET', 'POST'])
def owner_reg():
    login = request.form.get('login')
    password = request.form.get('password')
    if not login is None and not password is None and email_validate.validate(login):
        connection.OWNER_reg(login, password)
        return redirect('/owner_login')
    return render_template('registration.html', title='Авторизация', logo=logo, 
                           owners=owners, arrow=arrow, style=style,
                            bg=bg, script=script, validation=validation)

@app.route('/success', methods=['GET', 'POST'])
def success():
    if session['is_log']:
        name = request.form.get('name')
        adress = request.form.get('adress')
        cost = request.form.get('cost')
        count_places = request.form.get('count_places')
        if (not name is None and not adress is None and
            not cost is None and not count_places is None):
            cost = int(cost)
            count_places = int(count_places)
            connection.add_PARKING(name, adress, cost, count_places)
        return render_template('lk.html', logo=logo, add_parking=add_parking,
                            owners=owners, arrow=arrow, style=style,
                                bg=bg, script=script, validation=validation, name=name,
                                adress=adress, cost=cost, count_places=count_places)
    else:
        return '<h1>AСCESS DENIED</h1>'

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    parkings = connection.return_PARKINGS()
    return render_template('parking_list.html', parkings=parkings, logo=logo, add_parking=add_parking,
                           owners=owners, arrow=arrow, style=style, server=server,
                            bg=bg)
    
@app.route('/<id_>', methods=['GET', 'POST'])
def booking_list(id_):
    parking = connection.return_PARKINGS_id(str(id_))
    parking.append(connection.return_place_count(str(id_)))
    parking.append('есть свободные места' if connection.return_free_places(str(id_)) else 'свободных мест нет')
    email = request.form.get('email')
    if email:
        if email_validate.validate(email):
            code, QR = create_qr(id_, server)
            code = f'static/QR/{code}.png'
            return render_template('qr.html', code=code, logo=logo, add_parking=add_parking,
                                    owners=owners, arrow=arrow, style=style, server=server,
                                        bg=bg)
    return render_template('parking.html', parkings=parking, logo=logo, add_parking=add_parking,
                           owners=owners, arrow=arrow, style=style,
                            bg=bg)


if __name__ == '__main__':
    app.run(port=port, host=host)
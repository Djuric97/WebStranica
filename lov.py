from flask import Flask, render_template, request, session, redirect, url_for
import flask_bootstrap
import flask
from flask_mysqldb import MySQL
import yaml
import hashlib



aplikacija = Flask(__name__)
aplikacija.secret_key = b'krcmarice1'
flask_bootstrap.Bootstrap(aplikacija)

baza = yaml.safe_load(open('baza.yaml'))
aplikacija.config['MYSQL_HOST'] = baza['mysql_host']
aplikacija.config['MYSQL_USER'] = baza['mysql_user']
aplikacija.config['MYSQL_PASSWORD'] = baza['mysql_password']
aplikacija.config['MYSQL_DB'] = baza['mysql_db']

mysql = MySQL(aplikacija)


#Pocetna i Podrucje
@aplikacija.route('/')
def pocetna():
    return render_template('pocetna.html')

@aplikacija.route('/podrucje')
def podrucje():
    if request.method == 'GET':
        kurzor = mysql.connection.cursor()
        kurzor.execute('SELECT * FROM podrucje')
        oblast = kurzor.fetchall()
        return render_template('podrucje.html', oblast=oblast)
    else:
        return render_template('wrong.html')




#Zivotinje / Dodavanje
@aplikacija.route('/zivotinje', methods=['POST', 'GET'])
def zivotinje():
    if request.method == 'GET':
        kurzor = mysql.connection.cursor()
        kurzor.execute('SELECT * FROM zivotinja')
        zivotinja = kurzor.fetchall()
        return render_template('zivotinje.html', zivotinja=zivotinja)
    else:
        return render_template('wrong.html')

@aplikacija.route('/dodaj_zivotinju', methods=['POST', 'GET'])
def dodavanje_zivotinje():
    if request.method == 'POST' and session.get('korisnicko'):
        kurzor = mysql.connection.cursor()
        vrsta = request.form.get('vrsta')
        opis = request.form.get('opis')
        slika = putanja()
        kurzor.execute("INSERT INTO zivotinja (vrsta, opis, slika) VALUES (%s, %s, %s)",
                       [vrsta, opis, slika])
        mysql.connection.commit()
        zivotinja = kurzor.fetchall()
        return redirect(url_for('zivotinje'))
    else:
        return render_template('dodaj_zivotinju.html')




#Vozila / Dodavanje
@aplikacija.route('/vozila', methods=['POST', 'GET'])
def vozila():
    if request.method == 'GET':
        kurzor = mysql.connection.cursor()
        kurzor.execute('SELECT * FROM vozilo')
        vozilo = kurzor.fetchall()
        return render_template('vozila.html', vozilo=vozilo)
    else:
        return render_template('wrong.html')

@aplikacija.route('/dodaj_vozilo', methods=['POST', 'GET'])
def dodavanje_vozila():
    if request.method == 'POST' and session.get('korisnicko'):
        kurzor = mysql.connection.cursor()
        model = request.form.get('model')
        opis = request.form.get('opis')
        slika = putanja()
        kurzor.execute("INSERT INTO vozilo (model, opis, slika) VALUES (%s, %s, %s)",
                       [model, opis, slika])
        mysql.connection.commit()
        vozilo = kurzor.fetchall()
        return redirect(url_for('vozila'))
    else:
        return render_template('dodaj_vozilo.html')




#Oruzje / Dodavanje
@aplikacija.route('/oruzje', methods=['POST', 'GET'])
def oruzje():
    if request.method == 'GET':
        kurzor = mysql.connection.cursor()
        kurzor.execute('SELECT * FROM oruzje')
        puska = kurzor.fetchall()
        return render_template('oruzje.html', puska=puska)
    else:
        return render_template('wrong.html')

@aplikacija.route('/dodavanje', methods=['POST', 'GET'])
def dodavanje():
    if request.method == 'POST' and session.get('korisnicko'):
        kurzor = mysql.connection.cursor()
        model = request.form.get('model')
        opis = request.form.get('opis')
        slika = putanja()
        kurzor.execute("INSERT INTO oruzje (model, opis, slika) VALUES (%s, %s, %s)",
                       [model, opis, slika])
        mysql.connection.commit()
        puska = kurzor.fetchall()
        return redirect(url_for('oruzje'))
    else:
        return render_template('dodavanje.html')




#Za upisivanje putanje slike u Bazu
def putanja():
    fotka = request.form.get('slika')
    return str("static/" + fotka)



#Autentifikacija admina / Uredjivanje profila
@aplikacija.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('korisnicko') is not None:
        kurzor = mysql.connection.cursor()
        kurzor.execute('UPDATE admin SET aktivan = 0 WHERE korisnicko = %s', [session['korisnicko']])
        mysql.connection.commit()
        session.pop('korisnicko')
        return render_template('pocetna.html')
    else:
        return redirect(url_for('login'))

@aplikacija.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('korisnicko') is None:
            kurzor = mysql.connection.cursor()
            kor_ime = request.form.get('korisnicko')
            pword = request.form.get('sifra')
            s = hashlib.sha256(pword.encode('ascii')).hexdigest()
            if kurzor.execute('SELECT * FROM admin WHERE korisnicko = %s AND sifra = %s', [kor_ime, s]) > 0:
                admin = kurzor.fetchone()
                session['ulogovan'] = True
                session['korisnicko'] = admin[1]
                mysql.connection.commit()
                kurzor.execute('UPDATE admin SET aktivan = 1 WHERE korisnicko = %s', [kor_ime])
                mysql.connection.commit()
                return render_template("pocetna.html")
            else:
                return render_template("login.html")
        else:
            return render_template("pocetna.html")
    else:
        return render_template('login.html')

@aplikacija.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if request.method == 'POST':
        kurzor = mysql.connection.cursor()

        korisnicko = request.form.get('korisnicko')
        ime = request.form.get('ime')
        prezime = request.form.get('prezime')
        email = request.form.get('email')
        sifra = request.form.get('sifra')
        potvrda_sifre = request.form.get('potvrdaSifre')
        if sifra == potvrda_sifre:
            s = hashlib.sha256(sifra.encode('ascii')).hexdigest()
            if kurzor.execute('SELECT * FROM admin WHERE email = %s', [email]) == 0:
                kurzor.execute("INSERT INTO admin (korisnicko, ime, prezime, email, sifra) VALUES (%s, %s, %s, %s, %s)",
                                [korisnicko, ime, prezime, email, s])
                mysql.connection.commit()
                kurzor.close()
                return redirect(url_for('pocetna'))
            else:
                flask.flash('Email exists!', 'danger')
                return render_template('registracija.html')
        else:
            flask.flash('Password error!')
            return render_template('registracija.html')
    return render_template('registracija.html')


@aplikacija.route('/izmjena', methods=['POST', 'GET'])
def izmjena():
    if request.method == 'POST':
        kurzor = mysql.connection.cursor()
        stara_v = request.form.get('stara')
        nova_v = request.form.get('nova')
        if request.form.get('opcija') == 'user':
            if session.get('korisnicko'):
                kurzor.execute(f'UPDATE admin SET korisnicko = "{nova_v}" WHERE korisnicko = "{stara_v}"')
                mysql.connection.commit()
                kurzor.close()
                return redirect(url_for('pocetna'))

        elif request.form.get('opcija') == 'sifra':
            if session.get('korisnicko'):
                kurzor.execute(f'UPDATE admin SET sifra = "{nova_v}" WHERE sifra = "{stara_v}"')
                mysql.connection.commit()
                kurzor.close()
                return redirect(url_for('pocetna'))

        elif request.form.get('opcija') == 'ime':
            if session.get('korisnicko'):
                kurzor.execute(f'UPDATE admin SET ime = "{nova_v}" WHERE ime = "{stara_v}"')
                mysql.connection.commit()
                kurzor.close()
                return redirect(url_for('pocetna'))

        elif request.form.get('opcija') == 'prezime':
            if session.get('korisnicko'):
                kurzor.execute(f'UPDATE admin SET prezime = "{nova_v}" WHERE prezime = "{stara_v}"')
                mysql.connection.commit()
                kurzor.close()
                return redirect(url_for('pocetna'))

        else:
            return redirect(url_for('oruzje'))
    return render_template('izmjena.html')


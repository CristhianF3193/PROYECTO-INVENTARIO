from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Mysql Connection
app = Flask(__name__)
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        radios = request.form['radios']
        imei = request.form['imei']
        prosena = request.form['prosena']
        estatus = request.form['estatus']
        ubicacion = request.form['ubicacion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (radios, imei, prosena, estatus, ubicacion) VALUES (%s, %s, %s, %s, %s)", (radios, imei, prosena, estatus, ubicacion))
        mysql.connection.commit()
        flash('Equipo Agregado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        radios = request.form['radios']
        imei = request.form['imei']
        prosena = request.form['prosena']
        estatus = request.form['estatus']
        ubicacion = request.form['ubicacion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET radios = %s,
                imei = %s,
                prosena = %s,
                estatus = %s,
                ubicacion = %s
            WHERE id = %s
        """, (radios, imei, prosena, estatus, ubicacion, id))
        mysql.connection.commit()
        flash('Equipo Actualizado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Equipo Removido Exitosamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='template')
app.secret_key = 'many random bytes'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    search_query = request.args.get('search', '')  
    cur = mysql.connection.cursor()

    if search_query:
        cur.execute("""
            SELECT * FROM students 
            WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s OR modelo LIKE %s
        """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    else:
        cur.execute("SELECT * FROM students")

    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', students=data, search_query=search_query)

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            return redirect(url_for('admin'))
        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrectos")

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        modelo = request.form['modelo']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO students (name, email, phone, modelo, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, modelo, estado))
        mysql.connection.commit()
        flash("Datos insertados correctamente")
        return redirect(url_for('admin'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        modelo = request.form['modelo']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students 
            SET name=%s, email=%s, phone=%s, modelo=%s, estado=%s
            WHERE id=%s
        """, (name, email, phone, modelo, estado, id_data))
        mysql.connection.commit()
        flash("Datos actualizados correctamente")
        return redirect(url_for('admin'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    flash("Registro eliminado correctamente")
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True) 

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)

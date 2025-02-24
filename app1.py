from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__, template_folder='template')
app.secret_key = 'many random bytes'

# Datos en memoria (reemplazan la base de datos)
usuarios = [
    {"id": 1, "correo": "admin@example.com", "password": "admin123"}
]

students = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    search_query = request.args.get('search', '')
    
    # Filtrar estudiantes basado en la búsqueda
    if search_query:
        filtered_students = [
            student for student in students
            if (search_query.lower() in student['name'].lower() or
                search_query.lower() in student['email'].lower() or
                search_query.lower() in student['phone'].lower() or
                search_query.lower() in student['modelo'].lower())
        ]
    else:
        filtered_students = students

    return render_template('admin.html', students=filtered_students, search_query=search_query)

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        # Buscar el usuario en la lista de usuarios
        account = next((user for user in usuarios if user['correo'] == _correo and user['password'] == _password), None)

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

        # Crear un nuevo estudiante
        new_student = {
            "id": len(students) + 1,  # ID autoincremental
            "name": name,
            "email": email,
            "phone": phone,
            "modelo": modelo,
            "estado": estado
        }
        students.append(new_student)
        flash("Datos insertados correctamente")
        return redirect(url_for('admin'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = int(request.form['id'])
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        modelo = request.form['modelo']
        estado = request.form['estado']

        # Buscar y actualizar el estudiante
        for student in students:
            if student['id'] == id_data:
                student['name'] = name
                student['email'] = email
                student['phone'] = phone
                student['modelo'] = modelo
                student['estado'] = estado
                break

        flash("Datos actualizados correctamente")
        return redirect(url_for('admin'))

@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    # Eliminar el estudiante
    global students
    students = [student for student in students if student['id'] != id_data]
    flash("Registro eliminado correctamente")
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
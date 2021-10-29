#Librerias necesarias
from flask import Flask, request, jsonify
#Necesario el driver para conectarse a MYSQL
from flask_mysqldb import MySQL
#Poder interactuar con Angular
from flask_cors import CORS, cross_origin
#Archivo con las configuraciones
from config import config
from validaciones import *
# initializations
app = Flask(__name__)
CORS(app)
# Conexion a MYSQL
mysql = MySQL(app)

# settings A partir de ese momento Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "mysecretkey"


# ruta para consultar todos los registros
@cross_origin()
@app.route('/getAll', methods = ['GET'])
def getAll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
       content = {'id': result[0], 'fullname': result[1], 'phone': result[2], 'email': result[3]}
       payload.append(content)
       content = {}
    return jsonify(payload)

# ruta para consultar por parametro
@cross_origin()
@app.route('/getAllById/<id>',methods = ['GET'])
def getAllById(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id LIKE %s', (id,))
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
       content = {'id': result[0], 'fullname': result[1], 'phone': result[2], 'email': result[3]}
       payload.append(content)
       content = {}
    return jsonify(payload)

#### ruta para crear un registro########
@cross_origin()
@app.route('/addContact', methods = ['POST'])
def add_contact():
    if(validar_nombre(request.json['fullname'])):
        try:
            if request.method == 'POST':
                fullname = request.json['fullname']  ## nombre
                phone = request.json['phone']        ## telefono
                email = request.json['email']        ## email
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO contactos (fullname, phone, email) VALUES (%s,%s,%s)", ( fullname, phone, email))
                mysql.connection.commit()
                return jsonify({"informacion":"Registro exitoso"})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Faltan datos por ingresar"})        

######### ruta para actualizar################
@cross_origin()
@app.route('/updateContact/<id>', methods = ['PUT'])
def update_contact(id):
    fullname = request.json['fullname']
    phone = request.json['phone']
    email = request.json['email']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contactos
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s """, (fullname, email, phone, id))
    mysql.connection.commit()
    return jsonify({"informacion":"Registro actualizado"})

####### ruta para eliminar registros
@cross_origin()
@app.route('/deleteContact/<id>', methods = ['DELETE'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({"informacion":"Registro eliminado"})


# starting the app
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run()

import re
from this import d
from flask import Flask,jsonify, redirect,request
from flask_mysqldb import MySQL
from decouple import config
from jose import jwt
from flask_cors import CORS


app = Flask(__name__)

mysql = MySQL(app)

app.config["MYSQL_HOST"]=config('MYSQL_HOST')
app.config["MYSQL_DB"]=config('MYSQL_DB')
app.config["MYSQL_USER"]=config('MYSQL_USER')
app.config["MYSQL_PASSWORD"]=config('MYSQL_PASSWORD')
app.config["MYSQL_PORT"]=int(config('MYSQL_PORT'))

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return redirect('https://documenter.getpostman.com/view/17377152/UVkjwHoQ')

@app.route('/usuarios',methods=['GET'])
def usuarios():

    cursor=mysql.connection.cursor()
    cursor.execute("select * FROM usuarios")
    data=cursor.fetchall()
    cursor.close()

    return jsonify(data)


@app.route('/usuario/<string:id>')
def usuario(id):

    cursor=mysql.connection.cursor()

    cursor.execute("select * FROM usuarios where id='{}'".format(id))
    data=cursor.fetchone()
    if(data):
         return jsonify(data)
    else:
        return jsonify({"Message":"Usuario no existe"})

@app.route('/usuario',methods=["POST"])
def create():

    data=request.json
    try:

        username=data["username"]
        password=data["password"]
        name=data["name"]
        cursor=mysql.connection.cursor()
        cursor.execute("select * FROM usuarios where username='{}'".format(username))
        data=cursor.fetchone()
        if(data):
            return jsonify({"Message":"Usuario con ese username ya esta registrado"})
        else:
            cursor.execute("INSERT INTO usuarios (name,username,password) VALUES ('{}','{}', '{}');".format(name,username,password))
            mysql.connection.commit()
            cursor.close()
            return jsonify({"Message":"Usuario Registrado con exito"})
    except :
        return jsonify({"Message":"Debes ingresar todos los campos "})


@app.route('/usuario/<int:id>',methods=['DELETE'])
def delete(id):
    cursor=mysql.connection.cursor()
    cursor.execute("select * FROM usuarios where id='{}'".format(id))
    data=cursor.fetchone()
    if(data): 
        cursor.execute("DELETE FROM usuarios WHERE id ='{}';".format(id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"Message":"Usuario Eliminado con exito"})
    else :
        return jsonify({"Message":"Usuario no encontrado"})

@app.route('/usuario/<int:id>', methods=["PUT"])
def update(id):
    data=request.json
    try:
       username=data["username"]
       password=data["password"]
       name=data["name"]
       cursor=mysql.connection.cursor()
       cursor.execute("select * FROM usuarios where id='{}'".format(id))
       data=cursor.fetchone()
       if(data):
           cursor.execute("UPDATE usuarios SET name = '{}',username = '{}', password = '{}' WHERE id='{}';".format(name,username,password,id))
           mysql.connection.commit()
           cursor.close()
           return jsonify({"Message":"Usuario Actualizado  con exito"})
       else:
           return jsonify({"Message":"Usuario no encontrado"})
    except :
        return jsonify({"Message":"Debes ingresar todos los campos "})

    


@app.route('/login', methods=['POST'])
def login():
    data=request.json
    username=data["username"]
    password=data["password"]
    cursor=mysql.connection.cursor()
    cursor.execute("select * from usuarios where username='{}' and password ='{}'".format(username, password))
    data=cursor.fetchone()
    if(data):
        token=jwt.encode({"id":data[0],"name":data[1],"username":data[2],"password":data[3]},config('KEY'), algorithm='HS256')
        return token
    else :
        return jsonify({"Message":"Credenciales Invalidas"})

@app.route('/decode', methods=['POST'])
def decode():
    token=request.headers["Token"]
    print(token)
    encode=jwt.decode(token,config('KEY'), algorithms=['HS256'])
    return jsonify(encode)

if __name__ == '__main__':
    app.run(debug=True)

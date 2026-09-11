from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

#INICIALIZAMOS NUESTA APP

app=Flask(__name__)

#CON ESTA PARTE HACEMOS LA COMNEXION CON LA BASE DE DATOS MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_pagina'


mysql=MySQL(app)
@app.route('/')
def index():
    cur=mysql.connect.cursor() 
    cur.execute("SELECT * FROM user") #EJECUTA LA CONSULTA DE MYSQL
    data= cur.fetchall() #recuperamos la informacion de nuestra bd
    cur.close() #CERRAMOS LA CONEXION
    return render_template ('index.html', user=data)

   
@app.route("/add", methods=['POST'])
def add_user():
    if request.method== 'POST':
        name=request.form['name']
        email=request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO user (name,email) VALUES (%s,%s)",(name,email))
        cur.close()
        return redirect(url_for('index'))
        #Create  CREAR
        #Read    LEER
        #Update  ACTUALIZAR
        #Delete  ELIMINAR
@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit_user(id):
    if request.method== 'POST':
        name=request.form['name']
        email=request.form['email']
        cur=mysql.connection.cursor()
        
        #se agrega WHERE id=%s para que solo se actualice y oincida con la tabla (name, email, id)
        cur.execute("UPDATE user SET name=%s, email=%s WHERE id=%s",(name,email,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index')) 
    else:
         cur=mysql.connection.cursor()
         cur.execute("SELECT * FROM user WHERE id=%s",(id,))#EJECUTA LA CONSULTA DE MYSQL
         data=cur.fetchone() #RECUPERAMOS LA INFORMACION DE MYSQL
         cur.close()
         return render_template('edit.html', user=data)
     
     
if __name__=='__main__':
    app.run(debug=True)
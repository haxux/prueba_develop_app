from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config
import traceback

app = Flask(__name__)

conexion=MySQL(app)

@app.route('/login/<string:login>/<string:password>')
def validar_login(login,password):
    try:
        cursor=conexion.connection.cursor()
        sql= "select username,contraseña from usuario where username = %s and contraseña=%s"
        cursor.execute(sql,(login,password))
        datos=cursor.fetchall()
        print(datos)
        if datos:
            return 'True'
        else:
            return 'False'
    except Exception as ex:
        traceback.print_exc()
        return("False")
    
@app.route('/home')
def home():
    return render_template('home.html')
        
@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
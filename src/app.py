from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import config
import traceback

app = Flask(__name__)
app.config.from_object(config['development'])
conexion = MySQL(app)

@app.route('/login/<string:login>/<string:password>')
def validar_login(login, password):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT username, contraseña FROM usuario WHERE username = %s AND contraseña = %s"
        cursor.execute(sql, (login, password))
        datos = cursor.fetchall()
        if datos:
            return 'valido'
        else:
            return 'invalido'
    except Exception as ex:
        traceback.print_exc()
        return "False"

@app.route('/home')
def home():
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT nombre, descripcion, precio_unitario, descuento,
                   (precio_unitario - (precio_unitario * descuento / 100)) AS precio_final
            FROM producto
            WHERE en_oferta = 1
        """)
        ofertas = cursor.fetchall()
        return render_template('home.html', ofertas=ofertas)
    except Exception as ex:
        traceback.print_exc()
        return "Error al cargar la página principal"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/productosCategoria/<categoria>')
def productosCategoria(categoria):
    return render_template('productosCategoria.html', categoria=categoria)


@app.route('/productos')
def productos():
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT p.id_producto, p.nombre, p.descripcion, p.precio_unitario, p.iva, c.nombre AS categoria
            FROM producto p
            INNER JOIN categoria c ON p.id_categoria = c.id_categoria
        """)
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos)
    except Exception as ex:
        traceback.print_exc()
        return "Error al cargar productos"

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    try:
        cursor = conexion.connection.cursor()
        
        # 🔹 Si es GET → mostrar el formulario
        if request.method == 'GET':
            cursor.execute("SELECT id_categoria, nombre FROM categoria")
            categorias = cursor.fetchall()
            return render_template('agregar_producto.html', categorias=categorias)
        
        # 🔹 Si es POST → procesar el formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_categoria = request.form['id_categoria']

        sql = """
            INSERT INTO producto (nombre, descripcion, precio_unitario, id_categoria)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, precio, id_categoria))
        conexion.connection.commit()
        return redirect(url_for('productos'))

    except Exception as ex:
        traceback.print_exc()
        return f"Error al agregar producto: {ex}"

@app.route('/editar_categoria/<int:id_producto>', methods=['GET', 'POST'])
def editar_categoria(id_producto):
    try:
        cursor = conexion.connection.cursor()

        if request.method == 'GET':
            # Obtener producto actual y todas las categorías
            cursor.execute("SELECT id_producto, nombre, id_categoria FROM producto WHERE id_producto = %s", (id_producto,))
            producto = cursor.fetchone()
            cursor.execute("SELECT id_categoria, nombre FROM categoria")
            categorias = cursor.fetchall()
            return render_template('editar_categoria.html', producto=producto, categorias=categorias)
        
        # Si es POST, actualizar la categoría
        nueva_categoria = request.form['id_categoria']
        cursor.execute("UPDATE producto SET id_categoria = %s WHERE id_producto = %s", (nueva_categoria, id_producto))
        conexion.connection.commit()
        return redirect(url_for('productos'))

    except Exception as ex:
        traceback.print_exc()
        return f"Error al cambiar la categoría: {ex}"
 

@app.route('/categorias')
def categorias():
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria")
        categorias = cursor.fetchall()
        return render_template('categorias.html', categorias=categorias)
    except Exception as ex:
        traceback.print_exc()
        return "Error al cargar categorías"

# 🔹 Ver productos por categoría
@app.route('/categoria/<int:id_categoria>')
def ver_categoria(id_categoria):
    try:
        cursor = conexion.connection.cursor()

        # 1️⃣ Obtener nombre de la categoría
        sql = "SELECT nombre FROM categoria WHERE id_categoria = %s"
        categoria = cursor.execute(sql,(id_categoria,))
        datos = cursor.fetchall()
        
        
        if not datos:
            return f"No se encontró la categoría con ID {id_categoria}"
        else:
        # 2️⃣ Obtener productos de esa categoría (ahora incluye nombre de categoría)
  
            sql = "SELECT p.id_producto, p.nombre, p.descripcion, c.nombre AS categoria, p.precio_unitario, p.iva FROM producto p INNER JOIN categoria c ON p.id_categoria = c.id_categoria WHERE p.id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            
            datos = cursor.fetchall()
            
            if not datos:
                return f"No se encontró la categoría con ID {id_categoria}"
            else:
                print("Productos encontrados:")
                
                return {"productos": datos }     

        # 3️⃣ Renderizar la plantilla
        #return render_template('categoria_detalle.html', categoria=categoria[0], productos=productos)

        #return {
        #"id_producto": id_producto,
        #"nombreProdunombre_productocto": nombre_producto
        
    #}

    except Exception as ex:
        import traceback
        traceback.print_exc()
        return f"❌ Error al cargar productos de la categoría {id_categoria}"



@app.route('/compras')
def compras():
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT id_producto, nombre, precio_unitario, iva FROM producto")
        productos = cursor.fetchall()
        return render_template('compras.html', productos=productos)
    except Exception as ex:
        traceback.print_exc()
        return "Error al cargar carrito"

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = '9902562'  # clave secreta 

# Inicializa la sesión si no existe
@app.before_request
def initialize_session():
    if 'productos' not in session:
        session['productos'] = []

# Función para verificar si el ID del producto es único
def id_unico(id):
    for producto in session['productos']:
        if producto['id'] == id:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }

        # Verifica si el ID es único
        if id_unico(nuevo_producto['id']):
            session['productos'].append(nuevo_producto)
            session.modified = True  # Indica que la sesión ha sido modificada
            flash('Producto agregado exitosamente', 'success')
        else:
            flash('El ID del producto debe ser único', 'error')

        return redirect(url_for('index'))

@app.route('/eliminar_producto/<string:producto_id>')
def eliminar_producto(producto_id):
    session['productos'] = [producto for producto in session['productos'] if producto['id'] != producto_id]
    session.modified = True  # Indica que la sesión ha sido modificada
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/editar_producto/<string:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    # Busca el producto por ID
    producto = next((p for p in session['productos'] if p['id'] == producto_id), None)

    if request.method == 'POST':
        # Actualiza el producto con los nuevos datos
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        
        session.modified = True  # Indica que la sesión ha sido modificada
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('index'))

    return render_template('editar_producto.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)

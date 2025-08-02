from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from psycopg2 import OperationalError

app = Flask(__name__)

# Configuración PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'db'),
            database=os.getenv('POSTGRES_DB', 'mydb'),
            user=os.getenv('POSTGRES_USER', 'user'),
            password=os.getenv('POSTGRES_PASSWORD', 'password')
        )
        return conn
    except OperationalError as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        if conn is None:
            return "Error de conexión a la base de datos", 500
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios;')
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', usuarios=usuarios)
    except Exception as e:
        print(f"Error en la ruta principal: {e}")
        return f"Error interno: {str(e)}", 500

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        nombre = request.form['nombre']
        celular = request.form['celular']
        
        conn = get_db_connection()
        if conn is None:
            return "Error de conexión a la base de datos", 500
            
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO usuarios (nombre, celular) VALUES (%s, %s)',
            (nombre, celular)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error al guardar datos: {e}")
        return f"Error al procesar el formulario: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
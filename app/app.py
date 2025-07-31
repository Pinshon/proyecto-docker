from flask import Flask, render_template
import redis
import psycopg2
import os

app = Flask(__name__)

# Configuración
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = 6379
redis_db = redis.Redis(host=redis_host, port=redis_port, db=0)

# Configuración PostgreSQL
db_host = os.getenv('POSTGRES_HOST', 'db')
db_name = os.getenv('POSTGRES_DB', 'mydb')
db_user = os.getenv('POSTGRES_USER', 'user')
db_pass = os.getenv('POSTGRES_PASSWORD', 'password')

@app.route('/')
def index():
    # Incrementar contador en Redis
    redis_db.incr('hits')
    
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return render_template('index.html', 
                         hits=redis_db.get('hits').decode('utf-8'),
                         db_version=db_version)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
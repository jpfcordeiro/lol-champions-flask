from flask import Flask, render_template, session, request, redirect
import pymysql
from controllers import routes
# Importando o model
from models.database import db
# Importando a biblioteca OS (comandos de S.O)
import os
from pymysql import connect

# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)

DB_NAME = 'champions'
app.config['DATABASE_NAME'] = DB_NAME

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root@localhost/{DB_NAME}'

# Secret para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Iniciar o servidor
if __name__ == '__main__':
    # Conecta mysql
    connection = connect(host='localhost', user='root',
                         password='', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')
    finally:
        connection.close()
        
    db.init_app(app=app)
    with app.test_request_context():
            db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

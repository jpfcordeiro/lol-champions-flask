import os
from flask import Flask
from controllers import routes
from models.database import db
import pymysql
from pymysql.cursors import DictCursor


app = Flask(__name__, template_folder='views')

app.secret_key = 'lolchampions'  

routes.init_app(app)

# Database configuration
DB_NAME = 'champions'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root@localhost/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create database if it doesn't exist
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    charset='utf8mb4',
    cursorclass=DictCursor
)
try:
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.commit()
finally:
    connection.close()

if __name__ == '__main__':
    db.init_app(app=app)
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=4000, debug=True)

import os
from flask import Flask
from controllers import routes
from models.database import db
from dotenv import load_dotenv
import pymysql

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='views')

routes.init_app(app)

# Database configuration
DB_NAME = os.getenv('DB_NAME', 'champions')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')

# Create database if it doesn't exist
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
try:
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.commit()
finally:
    connection.close()

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__ == '__main__':
    db.init_app(app=app)
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=4000, debug=True)
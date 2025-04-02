from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder='views')

routes.init_app(app)

DB_NAME = 'champions'
app.config['DATABASE_NAME'] = DB_NAME

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root@localhost/{DB_NAME}'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if (__name__) == '__main__':
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=4000, debug=True)
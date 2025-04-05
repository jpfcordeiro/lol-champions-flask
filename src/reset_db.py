import os
from app import app, db
from models.database import Champion, Gallery

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database reset successfully!")

if __name__ == '__main__':
    reset_database() 
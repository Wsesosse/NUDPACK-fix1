
import os
import sys

# Add the project root to sys.path so we can import 'server' module
sys.path.append(os.getcwd())

from server.app.db import engine, Base, init_db
from server.app.models import *  # Import all models to ensure they are registered

def reset_database():
    print("=====================================================")
    print("WARNING: This will PERMANENTLY DELETE current data!")
    print("ALL tables will be dropped and recreated.")
    print("=====================================================")
    confirm = input("Are you sure you want to proceed? (Type 'YES' to confirm): ")
    
    if confirm == "YES":
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Re-initializing database...")
        init_db()
        print("✅ Database reset complete!")
    else:
        print("❌ Action cancelled.")

if __name__ == "__main__":
    reset_database()

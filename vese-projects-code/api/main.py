from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

from routes import init_views 
from db import Database


# Load .env configuration file
load_dotenv()


app = Flask(__name__)

# Database setup
db = Database()
 
# Init routes
init_views(app,db)

if __name__ == '__main__':
    port = int(os.getenv("PORT")) if os.getenv("PORT") else 5000
    debug = os.getenv("DEBUG", 'False').lower() == 'true'
    
    app.run(debug=debug , port = port)

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    print("Allowing CORS for frontend URL:", frontend_url)
    CORS(app, resources={r"/*": {"origins": frontend_url}})
    
    from .routes import main
    app.register_blueprint(main)
    
    return app

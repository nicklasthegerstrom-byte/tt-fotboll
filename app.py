# app.py
from flask import Flask
from web.routes import web_bp

def create_app():
    app = Flask(__name__)
    
    # Kryptering för sessions så att redaktionen kan köra olika matcher samtidigt
    app.secret_key = 'tt-redaktionen-super-hemlig-kod-2026'
    
    # Registrera vår Blueprint som innehåller alla dörrar/rutter
    app.register_blueprint(web_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Vi kör på port 5000 i utvecklingsläge
    app.run(port=5000, debug=True)
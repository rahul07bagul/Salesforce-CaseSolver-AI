from flask import Flask
from routes.routes import case_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*")

    app.register_blueprint(case_routes, url_prefix='/api/v1/cases')
    print("Flask app initialized and routes registered.")
    return app

if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)

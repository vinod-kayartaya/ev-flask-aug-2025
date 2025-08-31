from flask import Flask
from config import Config
from extensions import db
from customers.routes import customers_bp
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(customers_bp)

    # Initialize Swagger
    swagger = Swagger(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8080)
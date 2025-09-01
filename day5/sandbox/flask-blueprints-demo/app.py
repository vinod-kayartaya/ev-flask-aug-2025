from flask import Flask
from config import Config
from extensions import db
from customers.routes import customers_bp
from categories.routes import cat_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(customers_bp)
    app.register_blueprint(cat_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8080)
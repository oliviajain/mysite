import os
from flask import Flask, render_template
from config import DevConfig, ProdConfig


def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'production':
        ProdConfig.validate()
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    from journal.database import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    from cookbook.routes import cookbook_bp
    from journal.routes import journal_bp
    from car.routes import car_bp
    from wedding.routes import wedding_bp
    
    app.register_blueprint(cookbook_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(wedding_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(port=port)

from flask import Flask
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # Importe o Flask-CORS
from models import db
from config import Config
from routes.user_routes import user_bp
from routes.departamento_routes import departamento_bp
from routes.auth_routes import auth_bp  

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "UserHub API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(auth_bp)  
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(departamento_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
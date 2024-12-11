from flask import Blueprint, jsonify, request
from services.auth_service import AuthService
from models import Usuario, db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'senha')):
        return jsonify({"status": "error", "response": "Dados inválidos"}), 400

    try:
        token, exp = AuthService.autenticar(data['email'], data['senha'])
        return jsonify({
            "status": "success",
            "token": token,
            "expires_at": exp.isoformat() + "Z"
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "response": str(e)}), 401

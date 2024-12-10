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

@auth_bp.route('/alterar_senha', methods=['POST'])
def alterar_senha():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"status": "error", "response": "Token não fornecido"}), 403

    try:
        token_data = AuthService.verificar_token(token.split(" ")[1])
        usuario_id = token_data['sub']
        data = request.get_json()
        if not data or 'nova_senha' not in data:
            return jsonify({"status": "error", "response": "Dados inválidos"}), 400
        
        usuario = Usuario.query.get(usuario_id)
        usuario.set_password(data['nova_senha'])
        db.session.commit()

        return jsonify({"status": "success", "response": "Senha alterada com sucesso"}), 200
    except ValueError as e:
        return jsonify({"status": "error", "response": str(e)}), 403
from functools import wraps
from flask import request, jsonify
from services.auth_service import AuthService

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"status": "error", "response": "Token não fornecido"}), 403

        try:
            token = token.split(" ")[1]
            payload = AuthService.verificar_token(token)
        
            if payload.get('tipo_usuario') == 'admin':
                return f(*args, **kwargs)
            else:
                return jsonify({"status": "error", "response": "Acesso negado: somente administradores"}), 403
        except (ValueError, Exception) as e:
            return jsonify({"status": "error", "response": str(e)}), 403

    return decorated_function
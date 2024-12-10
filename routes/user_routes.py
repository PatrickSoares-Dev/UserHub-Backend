from flask import Blueprint, jsonify, request, abort
from services.user_service import UserService
from utils.decorators import admin_required 

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/usuarios', methods=['GET'])
@admin_required
def get_usuarios():
    usuarios = UserService.listar_todos()
    response = {
        "status": "success",
        "response": [usuario.as_dict() for usuario in usuarios]
    }
    return jsonify(response), 200

@user_bp.route('/usuario/<int:id>', methods=['GET'])
@admin_required
def get_usuario(id):
    try:
        usuario = UserService.buscar_por_id(id)
        response = {
            "status": "success",
            "response": usuario.as_dict()
        }
        return jsonify(response), 200
    except:
        return jsonify({"status": "error", "response": "Usuário não encontrado"}), 404

@user_bp.route('/usuario', methods=['POST'])
@admin_required
def create_usuario():
    data = request.get_json()
    if not data or not all(key in data for key in ('nome', 'email', 'senha', 'tipo_usuario')):
        return jsonify({"status": "error", "response": "Dados inválidos"}), 400

    novo_usuario = UserService.criar_usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
        tipo_usuario=data['tipo_usuario'],
        departamento_nome=data.get('departamento')
    )
    response = {
        "status": "success",
        "response": novo_usuario.as_dict()
    }
    return jsonify(response), 201

@user_bp.route('/usuario/<int:id>', methods=['PUT'])
@admin_required
def update_usuario(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "response": "Dados inválidos"}), 400

    try:        
        usuario_atualizado = UserService.atualizar_usuario(
            id=id,
            nome=data.get('nome'),
            email=data.get('email'),
            senha=data.get('senha'),
            tipo_usuario=data.get('tipo_usuario'),
            departamento_nome=data.get('departamento')
        )
        response = {
            "status": "success",
            "response": usuario_atualizado.as_dict()
        }
        return jsonify(response), 200
    except Exception as e:        
        return jsonify({"status": "error", "response": "Usuário não encontrado"}), 404

@user_bp.route('/usuario/<int:id>', methods=['DELETE'])
@admin_required
def delete_usuario(id):
    if UserService.deletar_usuario(id):
        return jsonify({"status": "success", "response": "Usuário deletado com sucesso"}), 204
    else:
        return jsonify({"status": "error", "response": "Usuário não encontrado"}), 404
from flask import Blueprint, jsonify, request
from services.departamento_service import DepartamentoService

departamento_bp = Blueprint('departamento', __name__, url_prefix='/api')

@departamento_bp.route('/departamento', methods=['GET'])
def get_departamentos():
    try:
        departamentos = DepartamentoService.listar_todos()
        response = {
            "status": "success",
            "response": [departamento.as_dict() for departamento in departamentos]
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

@departamento_bp.route('/departamento/<int:id>', methods=['GET'])
def get_departamento(id):
    try:
        departamento = DepartamentoService.buscar_por_id(id)
        response = {
            "status": "success",
            "response": departamento.as_dict()
        }
        return jsonify(response), 200
    except:
        return jsonify({"status": "error", "response": "Departamento não encontrado"}), 404
    
@departamento_bp.route('/departamento', methods=['POST'])
def create_departamento():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({"status": "error", "response": "Dados inválidos"}), 400

    try:
        novo_departamento = DepartamentoService.criar_departamento(data['nome'])
        response = {
            "status": "success",
            "response": novo_departamento.as_dict()
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({"status": "error", "response": str(e)}), 400


@departamento_bp.route('/departamento/<int:id>', methods=['PUT'])
def update_departamento(id):
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({"status": "error", "response": "Dados inválidos"}), 400

    try:
        departamento_atualizado = DepartamentoService.atualizar_departamento(id, data['nome'])
        response = {
            "status": "success",
            "response": departamento_atualizado.as_dict()
        }
        return jsonify(response), 200
    except:
        return jsonify({"status": "error", "response": "Departamento não encontrado"}), 404

@departamento_bp.route('/departamento/<int:id>', methods=['DELETE'])
def delete_departamento(id):
    if DepartamentoService.deletar_departamento(id):
        return jsonify({"status": "success", "response": "Departamento deletado com sucesso"}), 204
    else:
        return jsonify({"status": "error", "response": "Departamento não encontrado"}), 404
from flask import Blueprint, jsonify, request, abort
from services.departamento_service import DepartamentoService
from utils.decorators import admin_required 

departamento_bp = Blueprint('departamento', __name__, url_prefix='/api/departamentos')

@departamento_bp.route('/', methods=['GET'])
@admin_required
def get_departamentos():
    departamentos = DepartamentoService.listar_todos()
    response = {
        "status": "success",
        "response": [departamento.as_dict() for departamento in departamentos]
    }
    return jsonify(response), 200

@departamento_bp.route('/<int:id>', methods=['GET'])
@admin_required
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

@departamento_bp.route('/', methods=['POST'])
@admin_required
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

@departamento_bp.route('/<int:id>', methods=['PUT'])
@admin_required
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

@departamento_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_departamento(id):
    if DepartamentoService.deletar_departamento(id):
        return jsonify({"status": "success", "response": "Departamento deletado com sucesso"}), 204
    else:
        return jsonify({"status": "error", "response": "Departamento não encontrado"}), 404
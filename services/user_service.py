# services/user_service.py

from werkzeug.security import generate_password_hash
from models import db, Usuario, Departamento

class UserService:
    
    @staticmethod
    def listar_todos():
        return Usuario.query.all()

    @staticmethod
    def buscar_por_id(user_id):
        return Usuario.query.get_or_404(user_id)

    @staticmethod
    def criar_usuario(nome, email, senha, tipo_usuario, departamento_nome=None):
        departamento = None
        if departamento_nome:
            departamento = Departamento.query.filter_by(nome=departamento_nome).first()
            if not departamento:
                departamento = Departamento(nome=departamento_nome)
                db.session.add(departamento)
                db.session.flush()
                
        novo_usuario = Usuario(nome=nome, email=email, tipo_usuario=tipo_usuario, departamento=departamento)
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    @staticmethod
    def atualizar_usuario(id, nome=None, email=None, senha=None, tipo_usuario=None, departamento_nome=None):
        usuario = Usuario.query.get_or_404(id)

        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.set_password(senha)
        if tipo_usuario:
            usuario.tipo_usuario = tipo_usuario

        if departamento_nome:
            departamento = Departamento.query.filter_by(nome=departamento_nome).first()
            if not departamento:
                departamento = Departamento(nome=departamento_nome)
                db.session.add(departamento)
                db.session.flush()
            usuario.departamento = departamento

        db.session.commit()
        return usuario

    @staticmethod
    def deletar_usuario(id):
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False
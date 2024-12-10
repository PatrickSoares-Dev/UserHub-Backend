from models import db, Departamento

class DepartamentoService:
    
    @staticmethod
    def listar_todos():
        return Departamento.query.all()

    @staticmethod
    def buscar_por_id(departamento_id):
        return Departamento.query.get_or_404(departamento_id)

    @staticmethod
    def criar_departamento(nome):
        departamento_existente = Departamento.query.filter_by(nome=nome).first()
        if departamento_existente:
            raise ValueError("Departamento já existe")
        
        novo_departamento = Departamento(nome=nome)
        db.session.add(novo_departamento)
        db.session.commit()
        return novo_departamento

    @staticmethod
    def atualizar_departamento(id, nome):
        departamento = Departamento.query.get_or_404(id)
        departamento.nome = nome
        db.session.commit()
        return departamento

    @staticmethod
    def deletar_departamento(id):
        departamento = Departamento.query.get(id)
        if departamento:
            db.session.delete(departamento)
            db.session.commit()
            return True
        return False
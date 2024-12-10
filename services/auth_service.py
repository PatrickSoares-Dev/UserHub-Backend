import datetime
import jwt
import logging
from models import Usuario

class AuthService:
    SECRET_KEY = 'w4DbNMXaHuQDVgZ1zDFJqxAB3ArcEqay'

    @staticmethod
    def autenticar(email, senha):
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(senha):
            return AuthService.gerar_token(usuario)
        raise ValueError("Credenciais inválidas")

    @staticmethod
    def gerar_token(usuario):
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        payload = {
            'exp': exp,
            'iat': datetime.datetime.utcnow(),
            'sub': str(usuario.id),  # Converte o ID do usuário para string
            'nome': usuario.nome,
            'tipo_usuario': usuario.tipo_usuario,
            'email': usuario.email
        }
        token = jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        logging.info("Token gerado: %s", token)
        return token, exp

    @staticmethod      
    def verificar_token(token):
        try:
            logging.info("Verificando token: %s", token)
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=['HS256'])
            logging.info("Payload decodificado: %s", payload)
            if isinstance(payload, dict):
                return payload  # Retorna o payload completo
            else:
                raise ValueError("Payload não é um dicionário conforme esperado")
        except jwt.ExpiredSignatureError:
            logging.error("Token expirado")
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError as e:
            logging.error("Token inválido: %s", str(e))
            raise ValueError("Token inválido: %s" % str(e))
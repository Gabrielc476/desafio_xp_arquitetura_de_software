from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com pedidos (importação tardia)
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True, cascade='all, delete-orphan')

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.set_senha(senha)

    def set_senha(self, senha):
        # Gera hash da senha
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        # Verifica senha
        return check_password_hash(self.senha, senha)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'total_pedidos': len(self.pedidos)
        }

    def __repr__(self):
        return f'<Cliente {self.nome}>'
from db import db
from datetime import datetime

# Tabela de associação muitos-para-muitos
pedido_produto = db.Table('pedido_produto',
                          db.Column('pedido_id', db.Integer, db.ForeignKey('pedidos.id'), primary_key=True),
                          db.Column('produto_id', db.Integer, db.ForeignKey('produtos.id'), primary_key=True),
                          db.Column('quantidade', db.Integer, nullable=False, default=1),
                          db.Column('preco_unitario', db.Float, nullable=False)
                          )


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, index=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    # Relacionamento com pedidos (importação tardia)
    pedidos = db.relationship('Pedido', secondary=pedido_produto, back_populates='produtos')

    def __init__(self, nome, quantidade, preco, descricao=None):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.descricao = descricao

    def tem_estoque(self, quantidade_solicitada=1):
        # Verifica se há estoque suficiente
        return self.quantidade >= quantidade_solicitada and self.ativo

    def reduzir_estoque(self, quantidade):
        if not self.tem_estoque(quantidade):
            raise ValueError(f"Estoque insuficiente. Disponível: {self.quantidade}")
        self.quantidade -= quantidade

    def aumentar_estoque(self, quantidade):
        self.quantidade += quantidade

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'preco': float(self.preco),
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'ativo': self.ativo
        }

    def __repr__(self):
        return f'<Produto {self.nome}>'
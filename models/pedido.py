from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
from models.produto import pedido_produto

db = SQLAlchemy()


class StatusPedido(Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    PROCESSANDO = "PROCESSANDO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(StatusPedido), default=StatusPedido.PENDENTE, nullable=False)
    observacoes = db.Column(db.Text)

    # Relacionamento com produtos
    produtos = db.relationship('Produto', secondary=pedido_produto, back_populates='pedidos')

    def __init__(self, cliente_id, observacoes=None):
        self.cliente_id = cliente_id
        self.observacoes = observacoes
        self.total = 0.0

    def adicionar_produto(self, produto, quantidade=1):
        if not produto.tem_estoque(quantidade):
            raise ValueError(f"Estoque insuficiente para {produto.nome}")

        if produto not in self.produtos:
            self.produtos.append(produto)

        self.calcular_total()

    def remover_produto(self, produto_id):
        from models.produto import Produto
        produto = Produto.query.get(produto_id)
        if produto and produto in self.produtos:
            self.produtos.remove(produto)
            self.calcular_total()

    def calcular_total(self):
        # Calcula total baseado nos produtos
        total = 0.0
        for produto in self.produtos:
            total += produto.preco  # Assumindo quantidade 1 por simplicidade
        self.total = total
        return self.total

    def confirmar_pedido(self):
        if self.status != StatusPedido.PENDENTE:
            raise ValueError("Apenas pedidos pendentes podem ser confirmados")

        if not self.produtos:
            raise ValueError("Pedido deve ter ao menos um produto")

        # Reduz estoque dos produtos
        for produto in self.produtos:
            produto.reduzir_estoque(1)  # Quantidade fixa por simplicidade

        self.status = StatusPedido.CONFIRMADO

    def cancelar_pedido(self):
        if self.status in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
            raise ValueError("Pedido não pode ser cancelado no status atual")

        # Restaura estoque se já foi confirmado
        if self.status != StatusPedido.PENDENTE:
            for produto in self.produtos:
                produto.aumentar_estoque(1)

        self.status = StatusPedido.CANCELADO

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'total': float(self.total),
            'data': self.data.isoformat() if self.data else None,
            'status': self.status.value if self.status else None,
            'observacoes': self.observacoes,
            'produtos': [produto.to_dict() for produto in self.produtos],
            'quantidade_itens': len(self.produtos)
        }

    def __repr__(self):
        return f'<Pedido {self.id} - Total: R$ {self.total:.2f}>'
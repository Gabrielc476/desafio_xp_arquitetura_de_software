from models.pedido import Pedido, StatusPedido, db
from datetime import datetime
from typing import List, Optional


class PedidoRepository:

    @staticmethod
    def criar(pedido: Pedido) -> Pedido:
        db.session.add(pedido)
        db.session.commit()
        return pedido

    @staticmethod
    def buscar_por_id(pedido_id: int) -> Optional[Pedido]:
        return Pedido.query.get(pedido_id)

    @staticmethod
    def listar_todos() -> List[Pedido]:
        return Pedido.query.order_by(Pedido.data.desc()).all()

    @staticmethod
    def contar() -> int:
        return Pedido.query.count()

    @staticmethod
    def buscar_por_cliente(cliente_id: int) -> List[Pedido]:
        return Pedido.query.filter_by(cliente_id=cliente_id).order_by(Pedido.data.desc()).all()

    @staticmethod
    def buscar_por_status(status: StatusPedido) -> List[Pedido]:
        return Pedido.query.filter_by(status=status).order_by(Pedido.data.desc()).all()

    @staticmethod
    def buscar_por_periodo(data_inicio: datetime, data_fim: datetime) -> List[Pedido]:
        return Pedido.query.filter(
            Pedido.data >= data_inicio,
            Pedido.data <= data_fim
        ).order_by(Pedido.data.desc()).all()

    @staticmethod
    def atualizar(pedido: Pedido) -> Pedido:
        db.session.commit()
        return pedido

    @staticmethod
    def deletar(pedido: Pedido) -> None:
        db.session.delete(pedido)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
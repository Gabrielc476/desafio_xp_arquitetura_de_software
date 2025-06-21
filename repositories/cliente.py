from models.cliente import Cliente
from db import db
from typing import List, Optional


class ClienteRepository:

    @staticmethod
    def criar(cliente: Cliente) -> Cliente:
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def buscar_por_id(cliente_id: int) -> Optional[Cliente]:
        return Cliente.query.get(cliente_id)

    @staticmethod
    def buscar_por_email(email: str) -> Optional[Cliente]:
        return Cliente.query.filter_by(email=email).first()

    @staticmethod
    def buscar_por_nome(nome: str) -> List[Cliente]:
        return Cliente.query.filter(Cliente.nome.ilike(f'%{nome}%')).all()

    @staticmethod
    def listar_todos() -> List[Cliente]:
        return Cliente.query.all()

    @staticmethod
    def contar() -> int:
        return Cliente.query.count()

    @staticmethod
    def atualizar(cliente: Cliente) -> Cliente:
        db.session.commit()
        return cliente

    @staticmethod
    def deletar(cliente: Cliente) -> None:
        db.session.delete(cliente)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

from models.produto import Produto, db
from typing import List, Optional


class ProdutoRepository:

    @staticmethod
    def criar(produto: Produto) -> Produto:
        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def buscar_por_id(produto_id: int) -> Optional[Produto]:
        return Produto.query.get(produto_id)

    @staticmethod
    def buscar_por_nome(nome: str) -> List[Produto]:
        return Produto.query.filter(Produto.nome.ilike(f'%{nome}%')).all()

    @staticmethod
    def listar_todos(incluir_inativos: bool = False) -> List[Produto]:
        query = Produto.query
        if not incluir_inativos:
            query = query.filter_by(ativo=True)
        return query.all()

    @staticmethod
    def contar(incluir_inativos: bool = False) -> int:
        query = Produto.query
        if not incluir_inativos:
            query = query.filter_by(ativo=True)
        return query.count()

    @staticmethod
    def atualizar(produto: Produto) -> Produto:
        db.session.commit()
        return produto

    @staticmethod
    def deletar(produto: Produto) -> None:
        db.session.delete(produto)
        db.session.commit()

    @staticmethod
    def buscar_por_faixa_preco(preco_min: float, preco_max: float) -> List[Produto]:
        return Produto.query.filter(
            Produto.preco >= preco_min,
            Produto.preco <= preco_max,
            Produto.ativo == True
        ).all()

    @staticmethod
    def buscar_sem_estoque() -> List[Produto]:
        return Produto.query.filter_by(quantidade=0, ativo=True).all()

    @staticmethod
    def buscar_estoque_baixo(limite_estoque: int = 5) -> List[Produto]:
        return Produto.query.filter(
            Produto.quantidade <= limite_estoque,
            Produto.quantidade > 0,
            Produto.ativo == True
        ).all()

    @staticmethod
    def rollback():
        db.session.rollback()
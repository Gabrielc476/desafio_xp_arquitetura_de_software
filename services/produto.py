from models.produto import Produto
from repositories.produto import ProdutoRepository
from typing import List, Optional


class ProdutoService:

    def __init__(self):
        self.repository = ProdutoRepository()

    def criar_produto(self, nome: str, quantidade: int, preco: float,
                      descricao: str = None) -> Produto:
        self._validar_dados_produto(nome, quantidade, preco)

        try:
            produto = Produto(nome=nome, quantidade=quantidade, preco=preco, descricao=descricao)
            return self.repository.criar(produto)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao criar produto: {str(e)}")

    def buscar_produto_por_id(self, produto_id: int) -> Optional[Produto]:
        return self.repository.buscar_por_id(produto_id)

    def buscar_produtos_por_nome(self, nome: str) -> List[Produto]:
        if not nome or len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        return self.repository.buscar_por_nome(nome.strip())

    def listar_todos_produtos(self, incluir_inativos: bool = False) -> List[Produto]:
        return self.repository.listar_todos(incluir_inativos=incluir_inativos)

    def contar_produtos(self, incluir_inativos: bool = False) -> int:
        return self.repository.contar(incluir_inativos=incluir_inativos)

    def atualizar_produto(self, produto_id: int, nome: str = None,
                          quantidade: int = None, preco: float = None,
                          descricao: str = None, ativo: bool = None) -> Optional[Produto]:
        produto = self.repository.buscar_por_id(produto_id)
        if not produto:
            return None

        try:
            if nome is not None:
                self._validar_nome(nome)
                produto.nome = nome

            if quantidade is not None:
                self._validar_quantidade(quantidade)
                produto.quantidade = quantidade

            if preco is not None:
                self._validar_preco(preco)
                produto.preco = preco

            if descricao is not None:
                produto.descricao = descricao

            if ativo is not None:
                produto.ativo = ativo

            return self.repository.atualizar(produto)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao atualizar produto: {str(e)}")

    def deletar_produto(self, produto_id: int) -> bool:
        produto = self.repository.buscar_por_id(produto_id)
        if not produto:
            return False

        if produto.pedidos:
            raise ValueError("Não é possível deletar produto com pedidos associados")

        try:
            self.repository.deletar(produto)
            return True
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao deletar produto: {str(e)}")

    def ajustar_estoque(self, produto_id: int, nova_quantidade: int) -> Optional[Produto]:
        if nova_quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        return self.atualizar_produto(produto_id, quantidade=nova_quantidade)

    def obter_produtos_sem_estoque(self) -> List[Produto]:
        return self.repository.buscar_sem_estoque()

    def obter_produtos_estoque_baixo(self, limite_estoque: int = 5) -> List[Produto]:
        if limite_estoque <= 0:
            raise ValueError("Limite de estoque deve ser positivo")
        return self.repository.buscar_estoque_baixo(limite_estoque)

    def _validar_dados_produto(self, nome: str, quantidade: int, preco: float) -> None:
        self._validar_nome(nome)
        self._validar_quantidade(quantidade)
        self._validar_preco(preco)

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório")
        if len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")

    def _validar_quantidade(self, quantidade: int) -> None:
        if not isinstance(quantidade, int):
            raise ValueError("Quantidade deve ser um número inteiro")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")

    def _validar_preco(self, preco: float) -> None:
        if not isinstance(preco, (int, float)):
            raise ValueError("Preço deve ser um número")
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")
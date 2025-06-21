from models.pedido import Pedido, StatusPedido
from repositories.pedido import PedidoRepository
from services.cliente import ClienteService
from services.produto import ProdutoService
from typing import List, Optional


class PedidoService:

    def __init__(self):
        self.repository = PedidoRepository()
        self.cliente_service = ClienteService()
        self.produto_service = ProdutoService()

    def criar_pedido(self, cliente_id: int, observacoes: str = None) -> Pedido:
        cliente = self.cliente_service.buscar_cliente_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente com ID {cliente_id} não encontrado")

        try:
            pedido = Pedido(cliente_id=cliente_id, observacoes=observacoes)
            return self.repository.criar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao criar pedido: {str(e)}")

    def buscar_pedido_por_id(self, pedido_id: int) -> Optional[Pedido]:
        return self.repository.buscar_por_id(pedido_id)

    def listar_todos_pedidos(self) -> List[Pedido]:
        return self.repository.listar_todos()

    def contar_pedidos(self) -> int:
        return self.repository.contar()

    def buscar_pedidos_por_cliente(self, cliente_id: int) -> List[Pedido]:
        return self.repository.buscar_por_cliente(cliente_id)

    def buscar_pedidos_por_status(self, status: StatusPedido) -> List[Pedido]:
        return self.repository.buscar_por_status(status)

    def adicionar_produto_ao_pedido(self, pedido_id: int, produto_id: int,
                                    quantidade: int = 1) -> Optional[Pedido]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return None

        if pedido.status != StatusPedido.PENDENTE:
            raise ValueError("Só é possível adicionar produtos a pedidos pendentes")

        produto = self.produto_service.buscar_produto_por_id(produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado")

        if not produto.ativo:
            raise ValueError("Produto está inativo")

        if not produto.tem_estoque(quantidade):
            raise ValueError(f"Estoque insuficiente. Disponível: {produto.quantidade}")

        try:
            pedido.adicionar_produto(produto, quantidade)
            return self.repository.atualizar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao adicionar produto ao pedido: {str(e)}")

    def remover_produto_do_pedido(self, pedido_id: int, produto_id: int) -> Optional[Pedido]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return None

        if pedido.status != StatusPedido.PENDENTE:
            raise ValueError("Só é possível remover produtos de pedidos pendentes")

        try:
            pedido.remover_produto(produto_id)
            return self.repository.atualizar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao remover produto do pedido: {str(e)}")

    def confirmar_pedido(self, pedido_id: int) -> Optional[Pedido]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return None

        if pedido.status != StatusPedido.PENDENTE:
            raise ValueError("Apenas pedidos pendentes podem ser confirmados")

        if not pedido.produtos:
            raise ValueError("Pedido deve ter pelo menos um produto")

        try:
            pedido.confirmar_pedido()
            return self.repository.atualizar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao confirmar pedido: {str(e)}")

    def cancelar_pedido(self, pedido_id: int) -> Optional[Pedido]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return None

        try:
            pedido.cancelar_pedido()
            return self.repository.atualizar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao cancelar pedido: {str(e)}")

    def atualizar_status_pedido(self, pedido_id: int, novo_status: StatusPedido) -> Optional[Pedido]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return None

        try:
            pedido.status = novo_status
            return self.repository.atualizar(pedido)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao atualizar status: {str(e)}")

    def deletar_pedido(self, pedido_id: int) -> bool:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            return False

        if pedido.status not in [StatusPedido.PENDENTE, StatusPedido.CANCELADO]:
            raise ValueError("Só é possível deletar pedidos pendentes ou cancelados")

        try:
            self.repository.deletar(pedido)
            return True
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao deletar pedido: {str(e)}")
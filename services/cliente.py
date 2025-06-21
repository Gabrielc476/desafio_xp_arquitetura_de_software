from models.cliente import Cliente
from repositories.cliente import ClienteRepository
from typing import List, Optional
import re


class ClienteService:

    def __init__(self):
        self.repository = ClienteRepository()

    def criar_cliente(self, nome: str, email: str, senha: str) -> Cliente:
        self._validar_dados_cliente(nome, email, senha)

        if self.repository.buscar_por_email(email):
            raise ValueError(f"Email '{email}' já está em uso")

        try:
            cliente = Cliente(nome=nome, email=email, senha=senha)
            return self.repository.criar(cliente)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao criar cliente: {str(e)}")

    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
        return self.repository.buscar_por_id(cliente_id)

    def buscar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        if not nome or len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        return self.repository.buscar_por_nome(nome.strip())

    def listar_todos_clientes(self) -> List[Cliente]:
        return self.repository.listar_todos()

    def contar_clientes(self) -> int:
        return self.repository.contar()

    def atualizar_cliente(self, cliente_id: int, nome: str = None,
                          email: str = None, senha: str = None) -> Optional[Cliente]:
        cliente = self.repository.buscar_por_id(cliente_id)
        if not cliente:
            return None

        try:
            if nome is not None:
                self._validar_nome(nome)
                cliente.nome = nome

            if email is not None:
                self._validar_email(email)
                cliente_existente = self.repository.buscar_por_email(email)
                if cliente_existente and cliente_existente.id != cliente_id:
                    raise ValueError(f"Email '{email}' já está em uso")
                cliente.email = email

            if senha is not None:
                self._validar_senha(senha)
                cliente.set_senha(senha)

            return self.repository.atualizar(cliente)
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao atualizar cliente: {str(e)}")

    def deletar_cliente(self, cliente_id: int) -> bool:
        cliente = self.repository.buscar_por_id(cliente_id)
        if not cliente:
            return False

        if cliente.pedidos:
            raise ValueError("Não é possível deletar cliente com pedidos associados")

        try:
            self.repository.deletar(cliente)
            return True
        except Exception as e:
            self.repository.rollback()
            raise ValueError(f"Erro ao deletar cliente: {str(e)}")

    def autenticar_cliente(self, email: str, senha: str) -> Optional[Cliente]:
        cliente = self.repository.buscar_por_email(email)
        if cliente and cliente.check_senha(senha):
            return cliente
        return None

    def _validar_dados_cliente(self, nome: str, email: str, senha: str) -> None:
        self._validar_nome(nome)
        self._validar_email(email)
        self._validar_senha(senha)

    def _validar_nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório")
        if len(nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        if len(nome.strip()) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")

    def _validar_email(self, email: str) -> None:
        if not email or not email.strip():
            raise ValueError("Email é obrigatório")

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.strip()):
            raise ValueError("Email deve ter um formato válido")

        if len(email.strip()) > 120:
            raise ValueError("Email deve ter no máximo 120 caracteres")

    def _validar_senha(self, senha: str) -> None:
        if not senha:
            raise ValueError("Senha é obrigatória")
        if len(senha) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
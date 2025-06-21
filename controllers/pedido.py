from flask import Blueprint, request, jsonify
from services.pedido import PedidoService
from models.pedido import StatusPedido
from datetime import datetime
from typing import Dict, Any

# Criação do Blueprint para pedidos
pedido_bp = Blueprint('pedidos', __name__, url_prefix='/api/pedidos')

# Instância do serviço
pedido_service = PedidoService()


@pedido_bp.route('', methods=['GET'])
def listar_todos_pedidos():
    # GET /api/pedidos - Lista todos os pedidos
    try:
        pedidos = pedido_service.listar_todos_pedidos()
        return jsonify({
            'success': True,
            'data': [pedido.to_dict() for pedido in pedidos],
            'count': len(pedidos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar pedidos: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>', methods=['GET'])
def buscar_pedido_por_id(pedido_id: int):
    # GET /api/pedidos/{id} - Busca pedido por ID
    try:
        pedido = pedido_service.buscar_pedido_por_id(pedido_id)
        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': pedido.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar pedido: {str(e)}'
        }), 500


@pedido_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def buscar_pedidos_por_cliente(cliente_id: int):
    # GET /api/pedidos/cliente/{cliente_id} - Busca pedidos por cliente
    try:
        pedidos = pedido_service.buscar_pedidos_por_cliente(cliente_id)
        return jsonify({
            'success': True,
            'data': [pedido.to_dict() for pedido in pedidos],
            'count': len(pedidos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar pedidos: {str(e)}'
        }), 500


@pedido_bp.route('/status/<string:status>', methods=['GET'])
def buscar_pedidos_por_status(status: str):
    # GET /api/pedidos/status/{status} - Busca pedidos por status
    try:
        # Converter string para enum
        status_enum = StatusPedido(status.upper())
        pedidos = pedido_service.buscar_pedidos_por_status(status_enum)

        return jsonify({
            'success': True,
            'data': [pedido.to_dict() for pedido in pedidos],
            'count': len(pedidos),
            'status_filtrado': status_enum.value
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': f'Status inválido. Valores válidos: {[s.value for s in StatusPedido]}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar pedidos: {str(e)}'
        }), 500


@pedido_bp.route('/contar', methods=['GET'])
def contar_pedidos():
    # GET /api/pedidos/contar - Retorna o número total de pedidos
    try:
        total = pedido_service.contar_pedidos()
        return jsonify({
            'success': True,
            'total': total
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao contar pedidos: {str(e)}'
        }), 500


@pedido_bp.route('', methods=['POST'])
def criar_pedido():
    # POST /api/pedidos - Cria um novo pedido
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        # Validação de campos obrigatórios
        if 'cliente_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo cliente_id é obrigatório'
            }), 400

        pedido = pedido_service.criar_pedido(
            cliente_id=data['cliente_id'],
            observacoes=data.get('observacoes')
        )

        return jsonify({
            'success': True,
            'message': 'Pedido criado com sucesso',
            'data': pedido.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar pedido: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>/produtos', methods=['POST'])
def adicionar_produto_ao_pedido(pedido_id: int):
    # POST /api/pedidos/{id}/produtos - Adiciona produto ao pedido
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        # Validação de campos obrigatórios
        if 'produto_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo produto_id é obrigatório'
            }), 400

        pedido = pedido_service.adicionar_produto_ao_pedido(
            pedido_id=pedido_id,
            produto_id=data['produto_id'],
            quantidade=data.get('quantidade', 1)
        )

        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Produto adicionado ao pedido com sucesso',
            'data': pedido.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao adicionar produto: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>/produtos/<int:produto_id>', methods=['DELETE'])
def remover_produto_do_pedido(pedido_id: int, produto_id: int):
    # DELETE /api/pedidos/{pedido_id}/produtos/{produto_id} - Remove produto do pedido
    try:
        pedido = pedido_service.remover_produto_do_pedido(
            pedido_id=pedido_id,
            produto_id=produto_id
        )

        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Produto removido do pedido com sucesso',
            'data': pedido.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao remover produto: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>/confirmar', methods=['PUT'])
def confirmar_pedido(pedido_id: int):
    # PUT /api/pedidos/{id}/confirmar - Confirma um pedido
    try:
        pedido = pedido_service.confirmar_pedido(pedido_id)

        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Pedido confirmado com sucesso',
            'data': pedido.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao confirmar pedido: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>/cancelar', methods=['PUT'])
def cancelar_pedido(pedido_id: int):
    # PUT /api/pedidos/{id}/cancelar - Cancela um pedido
    try:
        pedido = pedido_service.cancelar_pedido(pedido_id)

        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Pedido cancelado com sucesso',
            'data': pedido.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao cancelar pedido: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>/status', methods=['PUT'])
def atualizar_status_pedido(pedido_id: int):
    # PUT /api/pedidos/{id}/status - Atualiza o status de um pedido
    try:
        data = request.get_json()

        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo status é obrigatório'
            }), 400

        # Converter string para enum
        novo_status = StatusPedido(data['status'].upper())

        pedido = pedido_service.atualizar_status_pedido(
            pedido_id=pedido_id,
            novo_status=novo_status
        )

        if not pedido:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Status do pedido atualizado com sucesso',
            'data': pedido.to_dict()
        }), 200

    except ValueError as e:
        if "Invalid enum value" in str(e) or "is not a valid StatusPedido" in str(e):
            return jsonify({
                'success': False,
                'message': f'Status inválido. Valores válidos: {[s.value for s in StatusPedido]}'
            }), 400
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar status: {str(e)}'
        }), 500


@pedido_bp.route('/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(pedido_id: int):
    # DELETE /api/pedidos/{id} - Deleta um pedido
    try:
        sucesso = pedido_service.deletar_pedido(pedido_id)

        if not sucesso:
            return jsonify({
                'success': False,
                'message': 'Pedido não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Pedido deletado com sucesso'
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar pedido: {str(e)}'
        }), 500


@pedido_bp.route('/status/opcoes', methods=['GET'])
def listar_status_opcoes():
    # GET /api/pedidos/status/opcoes - Lista todas as opções de status disponíveis
    try:
        opcoes = [{'value': status.value, 'name': status.name} for status in StatusPedido]
        return jsonify({
            'success': True,
            'data': opcoes
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar status: {str(e)}'
        }), 500


# Tratamento de erros específicos do blueprint
@pedido_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint não encontrado'
    }), 404


@pedido_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Método não permitido'
    }), 405
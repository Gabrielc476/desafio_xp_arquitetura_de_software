from flask import Blueprint, request, jsonify
from services.cliente import ClienteService
from typing import Dict, Any

# Criação do Blueprint para clientes
cliente_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

# Instância do serviço
cliente_service = ClienteService()


@cliente_bp.route('', methods=['GET'])
def listar_todos_clientes():
    # GET /api/clientes - Lista todos os clientes
    try:
        clientes = cliente_service.listar_todos_clientes()
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes],
            'count': len(clientes)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar clientes: {str(e)}'
        }), 500


@cliente_bp.route('/<int:cliente_id>', methods=['GET'])
def buscar_cliente_por_id(cliente_id: int):
    # GET /api/clientes/{id} - Busca cliente por ID
    try:
        cliente = cliente_service.buscar_cliente_por_id(cliente_id)
        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': cliente.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar cliente: {str(e)}'
        }), 500


@cliente_bp.route('/nome/<string:nome>', methods=['GET'])
def buscar_clientes_por_nome(nome: str):
    # GET /api/clientes/nome/{nome} - Busca clientes por nome
    try:
        clientes = cliente_service.buscar_clientes_por_nome(nome)
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes],
            'count': len(clientes)
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar clientes: {str(e)}'
        }), 500


@cliente_bp.route('/contar', methods=['GET'])
def contar_clientes():
    # GET /api/clientes/contar - Retorna o número total de clientes
    try:
        total = cliente_service.contar_clientes()
        return jsonify({
            'success': True,
            'total': total
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao contar clientes: {str(e)}'
        }), 500


@cliente_bp.route('', methods=['POST'])
def criar_cliente():
    # POST /api/clientes - Cria um novo cliente
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        # Validação de campos obrigatórios
        campos_obrigatorios = ['nome', 'email', 'senha']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo {campo} é obrigatório'
                }), 400

        cliente = cliente_service.criar_cliente(
            nome=data['nome'],
            email=data['email'],
            senha=data['senha']
        )

        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'data': cliente.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar cliente: {str(e)}'
        }), 500


@cliente_bp.route('/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id: int):
    # PUT /api/clientes/{id} - Atualiza um cliente existente
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        cliente = cliente_service.atualizar_cliente(
            cliente_id=cliente_id,
            nome=data.get('nome'),
            email=data.get('email'),
            senha=data.get('senha')
        )

        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Cliente não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso',
            'data': cliente.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar cliente: {str(e)}'
        }), 500


@cliente_bp.route('/<int:cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id: int):
    # DELETE /api/clientes/{id} - Deleta um cliente
    try:
        sucesso = cliente_service.deletar_cliente(cliente_id)

        if not sucesso:
            return jsonify({
                'success': False,
                'message': 'Cliente não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Cliente deletado com sucesso'
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar cliente: {str(e)}'
        }), 500


@cliente_bp.route('/login', methods=['POST'])
def autenticar_cliente():
    # POST /api/clientes/login - Autentica um cliente
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        # Validação de campos obrigatórios
        if 'email' not in data or 'senha' not in data:
            return jsonify({
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }), 400

        cliente = cliente_service.autenticar_cliente(
            email=data['email'],
            senha=data['senha']
        )

        if not cliente:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas'
            }), 401

        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'data': cliente.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro na autenticação: {str(e)}'
        }), 500


# Tratamento de erros específicos do blueprint
@cliente_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint não encontrado'
    }), 404


@cliente_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Método não permitido'
    }), 405
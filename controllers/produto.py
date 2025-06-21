from flask import Blueprint, request, jsonify
from services.produto import ProdutoService
from typing import Dict, Any

# Criação do Blueprint para produtos
produto_bp = Blueprint('produtos', __name__, url_prefix='/api/produtos')

# Instância do serviço
produto_service = ProdutoService()


@produto_bp.route('', methods=['GET'])
def listar_todos_produtos():
    # GET /api/produtos - Lista todos os produtos
    try:
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'
        produtos = produto_service.listar_todos_produtos(incluir_inativos=incluir_inativos)

        return jsonify({
            'success': True,
            'data': [produto.to_dict() for produto in produtos],
            'count': len(produtos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar produtos: {str(e)}'
        }), 500


@produto_bp.route('/<int:produto_id>', methods=['GET'])
def buscar_produto_por_id(produto_id: int):
    # GET /api/produtos/{id} - Busca produto por ID
    try:
        produto = produto_service.buscar_produto_por_id(produto_id)
        if not produto:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': produto.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produto: {str(e)}'
        }), 500


@produto_bp.route('/nome/<string:nome>', methods=['GET'])
def buscar_produtos_por_nome(nome: str):
    # GET /api/produtos/nome/{nome} - Busca produtos por nome
    try:
        produtos = produto_service.buscar_produtos_por_nome(nome)
        return jsonify({
            'success': True,
            'data': [produto.to_dict() for produto in produtos],
            'count': len(produtos)
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produtos: {str(e)}'
        }), 500


@produto_bp.route('/contar', methods=['GET'])
def contar_produtos():
    # GET /api/produtos/contar - Retorna o número total de produtos
    try:
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'
        total = produto_service.contar_produtos(incluir_inativos=incluir_inativos)
        return jsonify({
            'success': True,
            'total': total
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao contar produtos: {str(e)}'
        }), 500


@produto_bp.route('', methods=['POST'])
def criar_produto():
    # POST /api/produtos - Cria um novo produto
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        # Validação de campos obrigatórios
        campos_obrigatorios = ['nome', 'quantidade', 'preco']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo {campo} é obrigatório'
                }), 400

        produto = produto_service.criar_produto(
            nome=data['nome'],
            quantidade=data['quantidade'],
            preco=data['preco'],
            descricao=data.get('descricao')
        )

        return jsonify({
            'success': True,
            'message': 'Produto criado com sucesso',
            'data': produto.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar produto: {str(e)}'
        }), 500


@produto_bp.route('/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id: int):
    # PUT /api/produtos/{id} - Atualiza um produto existente
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON não fornecidos'
            }), 400

        produto = produto_service.atualizar_produto(
            produto_id=produto_id,
            nome=data.get('nome'),
            quantidade=data.get('quantidade'),
            preco=data.get('preco'),
            descricao=data.get('descricao'),
            ativo=data.get('ativo')
        )

        if not produto:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Produto atualizado com sucesso',
            'data': produto.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar produto: {str(e)}'
        }), 500


@produto_bp.route('/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id: int):
    # DELETE /api/produtos/{id} - Deleta um produto
    try:
        sucesso = produto_service.deletar_produto(produto_id)

        if not sucesso:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Produto deletado com sucesso'
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar produto: {str(e)}'
        }), 500


@produto_bp.route('/<int:produto_id>/estoque', methods=['PUT'])
def ajustar_estoque(produto_id: int):
    # PUT /api/produtos/{id}/estoque - Ajusta o estoque de um produto
    try:
        data = request.get_json()

        if not data or 'quantidade' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo quantidade é obrigatório'
            }), 400

        produto = produto_service.ajustar_estoque(
            produto_id=produto_id,
            nova_quantidade=data['quantidade']
        )

        if not produto:
            return jsonify({
                'success': False,
                'message': 'Produto não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Estoque ajustado com sucesso',
            'data': produto.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao ajustar estoque: {str(e)}'
        }), 500


@produto_bp.route('/sem-estoque', methods=['GET'])
def produtos_sem_estoque():
    # GET /api/produtos/sem-estoque - Lista produtos sem estoque
    try:
        produtos = produto_service.obter_produtos_sem_estoque()
        return jsonify({
            'success': True,
            'data': [produto.to_dict() for produto in produtos],
            'count': len(produtos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produtos sem estoque: {str(e)}'
        }), 500


@produto_bp.route('/estoque-baixo', methods=['GET'])
def produtos_estoque_baixo():
    # GET /api/produtos/estoque-baixo - Lista produtos com estoque baixo
    try:
        limite = int(request.args.get('limite', 5))
        produtos = produto_service.obter_produtos_estoque_baixo(limite_estoque=limite)
        return jsonify({
            'success': True,
            'data': [produto.to_dict() for produto in produtos],
            'count': len(produtos),
            'limite_aplicado': limite
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar produtos com estoque baixo: {str(e)}'
        }), 500


# Tratamento de erros específicos do blueprint
@produto_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint não encontrado'
    }), 404


@produto_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Método não permitido'
    }), 405
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

# Importar instância única do banco
from db import db

# Importar modelos (necessário para criar tabelas)
from models.cliente import Cliente
from models.produto import Produto
from models.pedido import Pedido

from controllers.cliente import cliente_bp
from controllers.produto import produto_bp
from controllers.pedido import pedido_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///desafio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)

@app.route('/')
def home():
    return jsonify({
        'message': 'API Desafio - Arquitetura MVC',
        'status': 'online',
        'endpoints': {
            'clientes': '/api/clientes',
            'produtos': '/api/produtos',
            'pedidos': '/api/pedidos'
        }
    })

with app.app_context():
    db.create_all()
    print("✅ Banco de dados inicializado!")

if __name__ == '__main__':
    app.run(debug=True)
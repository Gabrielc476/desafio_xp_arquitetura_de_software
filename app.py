from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Importar banco de dados dos modelos
from models.cliente import db

# Importar controllers
from controllers.cliente import cliente_bp
from controllers.produto import produto_bp
from controllers.pedido  import pedido_bp
# Criar aplicação Flask
app = Flask(__name__)

# Configurações básicas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///desafio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco de dados
db.init_app(app)

# Registrar rotas dos domínios
app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)

# Rota inicial
@app.route('/')
def home():
    return jsonify({
        'message': 'API desafio - Arquitetura MVC',
        'status': 'online',
        'endpoints': {
            'clientes': '/api/clientes',
            'produtos': '/api/produtos',
            'pedidos': '/api/pedidos'
        }
    })

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
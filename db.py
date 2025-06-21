# db.py - Instância única do SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

# Instância única do banco de dados
db = SQLAlchemy()
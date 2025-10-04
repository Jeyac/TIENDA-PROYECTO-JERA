from flask_sqlalchemy import SQLAlchemy

# Instancia única de SQLAlchemy para toda la app
db = SQLAlchemy()

__all__ = ["db"]



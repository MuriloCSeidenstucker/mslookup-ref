from flask import Flask

from mslookup_ref.main.routes.routes import medicine_route_bp

app = Flask(__name__)
"""Aplicação Flask principal.

Configura e inicializa a aplicação Flask, registrando o blueprint de rotas relacionadas
a medicamentos. Atua como o ponto de entrada da camada de apresentação, integrando as
rotas definidas no blueprint medicine_route_bp para processar requisições HTTP e retornar
respostas JSON.

Attributes:
    app (Flask): Instância da aplicação Flask configurada com o blueprint de rotas de medicamentos.
"""

app.register_blueprint(medicine_route_bp)

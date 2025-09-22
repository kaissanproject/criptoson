import logging
from flask import Flask, jsonify
from app.cache import cache
from app.limiter import limiter

# Configura o logging básico para exibir informações no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    """
    Fábrica de aplicação (Application Factory).
    Este padrão é útil para criar instâncias da aplicação com diferentes configurações,
    principalmente para testes.
    """
    app = Flask(__name__)

    # Configurações
    # Em um app real, isso viria de variáveis de ambiente ou um arquivo de config
    app.config["CACHE_TYPE"] = "SimpleCache"  # Cache em memória simples
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60   # Cache expira em 60 segundos

    # Inicializa as extensões com a aplicação
    cache.init_app(app)
    limiter.init_app(app)

    # Registra o Blueprint que contém as rotas
    from . import routes
    app.register_blueprint(routes.bp)

    # Adiciona um manipulador de erro global para a API CoinGecko
    # Se a API externa falhar, não quebramos o app, apenas mostramos um erro amigável.
    @app.errorhandler(ConnectionError)
    def handle_connection_error(e):
        logging.error(f"Erro de conexão com a API externa: {e}")
        # Para rotas de API, retorna JSON. Para páginas, poderia renderizar um template.
        if request.path.startswith('/api/'):
            return jsonify({"erro": "Não foi possível conectar à fonte de dados externa."}), 503
        # Para a interface do usuário, podemos renderizar uma página de erro
        return render_template("error.html", message="Estamos com problemas para buscar os dados. Tente novamente mais tarde."), 503

    return app

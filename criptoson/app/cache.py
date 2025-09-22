from flask_caching import Cache

# Instancia o objeto de cache que será inicializado na fábrica de aplicação.
# Usar um arquivo separado evita importações circulares.
cache = Cache()

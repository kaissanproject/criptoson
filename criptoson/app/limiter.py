from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Instancia o limiter. "get_remote_address" usa o IP do cliente para rastrear os limites.
# O limite padrão será definido no registro do blueprint de rotas.
limiter = Limiter(key_func=get_remote_address)

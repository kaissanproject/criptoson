from flask import Blueprint, render_template, request, jsonify
from .services import CoinGeckoService
from .cache import cache
from .limiter import limiter
import logging

# Cria um "Blueprint", que é uma forma de organizar um grupo de rotas relacionadas.
bp = Blueprint('main', __name__)
service = CoinGeckoService()

# --- Rotas da Interface do Usuário (HTML) ---

@bp.route('/')
@cache.cached(timeout=60, query_string=True) # Cacheia a resposta por 60s
def index():
    """ Rota da página inicial. """
    currency = request.args.get('currency', 'brl', type=str).lower()
    try:
        coins = service.get_top_coins(currency=currency)
        return render_template('index.html', coins=coins, currency=currency)
    except ConnectionError as e:
        logging.error(f"Falha ao carregar a página inicial: {e}")
        return render_template('index.html', coins=[], currency=currency, error="Não foi possível carregar os dados das moedas.")

@bp.route('/coin/<coin_id>')
@cache.cached(timeout=60, query_string=True) # Cacheia a resposta por 60s
def coin_detail(coin_id):
    """ Rota da página de detalhes de uma moeda. """
    currency = request.args.get('currency', 'brl', type=str).lower()
    try:
        coin = service.get_coin_details(coin_id, currency=currency)
        if not coin:
            return render_template('coin.html', error=f"Moeda '{coin_id}' não encontrada."), 404
        return render_template('coin.html', coin=coin, currency=currency)
    except ConnectionError as e:
        logging.error(f"Falha ao carregar detalhes da moeda {coin_id}: {e}")
        return render_template('coin.html', coin=None, currency=currency, error="Não foi possível carregar os dados da moeda.")


# --- Rotas da API (JSON) ---

@bp.route('/api/tickers')
@limiter.limit("20 per minute") # Limita a 20 chamadas por minuto por IP
@cache.cached(timeout=60, query_string=True)
def api_tickers():
    """ Endpoint da API para listar as top 50 moedas. """
    currency = request.args.get('currency', 'brl', type=str).lower()
    try:
        coins = service.get_top_coins(currency=currency)
        return jsonify(coins)
    except ConnectionError as e:
        return jsonify({"error": "Falha ao buscar dados da API externa", "message": str(e)}), 503

@bp.route('/api/coins/<coin_id>')
@limiter.limit("30 per minute")
@cache.cached(timeout=60, query_string=True)
def api_coin_detail(coin_id):
    """ Endpoint da API para detalhes de uma moeda específica. """
    currency = request.args.get('currency', 'brl', type=str).lower()
    try:
        coin = service.get_coin_details(coin_id, currency=currency)
        if not coin:
            return jsonify({"error": "Moeda não encontrada"}), 404
        return jsonify(coin)
    except ConnectionError as e:
        return jsonify({"error": "Falha ao buscar dados da API externa", "message": str(e)}), 503

@bp.route('/api/historical/<coin_id>')
@limiter.limit("30 per minute")
@cache.cached(timeout=60, query_string=True)
def api_historical_data(coin_id):
    """ Endpoint da API para dados históricos de uma moeda (para o gráfico). """
    currency = request.args.get('currency', 'brl', type=str).lower()
    days = request.args.get('days', 30, type=int)
    try:
        history = service.get_coin_market_chart(coin_id, currency=currency, days=days)
        if not history:
            return jsonify({"error": "Dados históricos não encontrados"}), 404
        return jsonify(history)
    except ConnectionError as e:
        return jsonify({"error": "Falha ao buscar dados da API externa", "message": str(e)}), 503

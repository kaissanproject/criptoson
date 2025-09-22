import pytest
from app import create_app
import json

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True
    # Desativa o cache e o rate limiting durante os testes para evitar interferências.
    app.config['CACHE_TYPE'] = 'NullCache'
    app.config['RATELIMIT_ENABLED'] = False

    with app.test_client() as client:
        yield client

def test_index_page(client, mocker):
    """Testa se a página inicial carrega corretamente."""
    # Mock para não fazer uma chamada real à API CoinGecko
    mocker.patch('app.services.CoinGeckoService.get_top_coins', return_value=[
        {'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}
    ])
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'Top 50 Criptomoedas' in response.data
    assert b'Bitcoin' in response.data

def test_api_tickers_endpoint(client, mocker):
    """Testa o endpoint /api/tickers."""
    mock_data = [{'id': 'bitcoin', 'name': 'Bitcoin', 'current_price': 150000}]
    mocker.patch('app.services.CoinGeckoService.get_top_coins', return_value=mock_data)

    response = client.get('/api/tickers?currency=brl')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert data == mock_data

def test_api_coin_detail_endpoint(client, mocker):
    """Testa o endpoint /api/coins/<id>."""
    mock_data = {'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'ETH'}
    mocker.patch('app.services.CoinGeckoService.get_coin_details', return_value=mock_data)

    response = client.get('/api/coins/ethereum')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Ethereum'

def test_api_coin_detail_not_found(client, mocker):
    """Testa o endpoint /api/coins/<id> para uma moeda inexistente."""
    mocker.patch('app.services.CoinGeckoService.get_coin_details', return_value=None)

    response = client.get('/api/coins/naoexiste')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_api_historical_endpoint(client, mocker):
    """Testa o endpoint /api/historical/<id>."""
    mock_data = {'prices': [[1672531200000, 16500.0], [1672617600000, 16600.0]]}
    mocker.patch('app.services.CoinGeckoService.get_coin_market_chart', return_value=mock_data)

    response = client.get('/api/historical/bitcoin?days=7')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prices' in data
    assert len(data['prices']) == 2

import requests
import logging

# Justificativa da API: CoinGecko é uma das APIs mais completas e confiáveis
# que oferece um plano gratuito generoso e sem a necessidade de chave de API para
# os endpoints que usaremos. Isso simplifica drasticamente a configuração para um iniciante.
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

class CoinGeckoService:
    """
    Esta classe encapsula toda a comunicação com a API da CoinGecko.
    Se um dia precisarmos trocar de provedor, só precisamos modificar esta classe.
    """

    def _make_request(self, endpoint, params=None):
        """
        Método auxiliar para fazer requisições à API e tratar erros comuns.
        """
        url = f"{COINGECKO_API_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10) # Timeout de 10s
            response.raise_for_status()  # Lança uma exceção para respostas com erro (4xx ou 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar a API CoinGecko em '{url}': {e}")
            # Lançamos uma ConnectionError para que a camada superior (rotas) possa tratá-la.
            raise ConnectionError(f"Não foi possível se conectar à API CoinGecko: {e}")

    def get_top_coins(self, currency='brl', limit=50):
        """
        Busca as top N moedas por capitalização de mercado.
        """
        params = {
            'vs_currency': currency,
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': 'false'
        }
        return self._make_request('coins/markets', params)

    def get_coin_details(self, coin_id, currency='brl'):
        """
        Busca os detalhes completos de uma moeda específica.
        """
        # A API de detalhes não aceita 'vs_currency', então buscamos os dados brutos
        # e depois pegamos o preço na moeda desejada.
        data = self._make_request(f'coins/{coin_id}')
        if not data:
            return None

        # Monta um dicionário com os dados que realmente vamos usar na interface
        details = {
            'id': data.get('id'),
            'symbol': data.get('symbol', '').upper(),
            'name': data.get('name'),
            'image': data.get('image', {}).get('large'),
            'description': data.get('description', {}).get('pt', 'Descrição não disponível em português.'),
            'market_data': {
                'current_price': data.get('market_data', {}).get('current_price', {}).get(currency),
                'market_cap': data.get('market_data', {}).get('market_cap', {}).get(currency),
                'total_volume': data.get('market_data', {}).get('total_volume', {}).get(currency),
                'price_change_percentage_24h': data.get('market_data', {}).get('price_change_percentage_24h_in_currency', {}).get(currency),
                'price_change_percentage_7d': data.get('market_data', {}).get('price_change_percentage_7d_in_currency', {}).get(currency),
            }
        }
        return details

    def get_coin_market_chart(self, coin_id, currency='brl', days=30):
        """
        Busca dados históricos para o gráfico de preços.
        """
        params = {
            'vs_currency': currency,
            'days': days,
            'interval': 'daily'
        }
        return self._make_request(f'coins/{coin_id}/market_chart', params)

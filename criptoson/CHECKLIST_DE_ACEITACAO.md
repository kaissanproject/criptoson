Checklist de Aceitação - Crypto Tracker
Use esta lista para validar se o projeto entregue atende a todos os requisitos solicitados.

Funcionalidades da Interface
[ ] Página Inicial (/):

[ ] Ao acessar http://localhost:5000, a página carrega sem erros.

[ ] A tabela exibe uma lista de criptomoedas (aproximadamente 50).

[ ] A tabela contém as colunas: #, Moeda, Preço, Variação 24h, Capitalização de Mercado.

[ ] Existe um campo de busca que filtra a tabela em tempo real ao digitar.

[ ] Clicar em uma linha da tabela redireciona para a página de detalhes daquela moeda.

[ ] Página de Detalhes (/coin/<id>):

[ ] Ao acessar http://localhost:5000/coin/bitcoin, a página carrega os dados do Bitcoin.

[ ] A página exibe o nome, símbolo, imagem e preço da moeda.

[ ] As métricas (Variação 24h, Volume, etc.) são exibidas.

[ ] Um gráfico de histórico de preços é exibido.

[ ] Os botões (7D, 30D, 90D) atualizam o gráfico com os dados do período correspondente.

[ ] Funcionalidades Gerais da UI:

[ ] Existe um seletor para mudar a moeda fiduciária (BRL, USD, EUR).

[ ] Mudar a moeda no seletor recarrega a página com os preços convertidos.

[ ] Existe um botão para alternar entre o tema claro e o escuro.

[ ] A interface é responsiva e se adapta bem a telas de celular.

Funcionalidades da API
[ ] Endpoint de Tickers (/api/tickers):

[ ] Acessar http://localhost:5000/api/tickers retorna uma resposta JSON com uma lista de moedas.

[ ] O status da resposta é 200 OK.

[ ] Endpoint de Detalhes (/api/coins/<id>):

[ ] Acessar http://localhost:5000/api/coins/ethereum retorna um objeto JSON com os detalhes do Ethereum.

[ ] Acessar um ID inválido (ex: /api/coins/naoexiste) retorna um erro 404 Not Found.

[ ] Endpoint de Histórico (/api/historical/<id>):

[ ] Acessar http://localhost:5000/api/historical/bitcoin?days=7 retorna um JSON com um array de prices.

[ ] O status da resposta é 200 OK.

Requisitos Técnicos
[ ] Cache:

[ ] Ao atualizar a página inicial várias vezes em menos de 60 segundos, os dados não mudam (indicando que o cache está funcionando). Após 60 segundos, os dados são atualizados.

[ ] Testes Automatizados:

[ ] O comando pytest executa sem erros e todos os testes passam.

[ ] Docker:

[ ] O comando docker-compose up --build inicia a aplicação com sucesso.

[ ] A aplicação fica acessível em http://localhost:5000 via Docker.

[ ] Documentação:

[ ] O README.md contém instruções claras para rodar o projeto com e sem Docker.

[ ] O arquivo requirements.txt lista todas as dependências necessárias.
Crypto Tracker - Guia de Deploy Online (Super Detalhado)
Bem-vindo! Este é um guia passo a passo, pensado para iniciantes, para colocar seu site de cotações de criptomoedas no ar. Vamos criar cada arquivo e pasta do zero e depois publicar tudo de graça.

O que vamos fazer:

(Passo 0) Criar a estrutura de pastas e arquivos: A parte mais importante! Vamos criar cada arquivo em seu devido lugar.

(Passo 1) Salvar o código no GitHub: O GitHub será nosso "cofre" online para o projeto.

(Passo 2) Conectar o Render ao GitHub: Vamos autorizar o Render a ler nosso código.

(Passo 3) Publicar o site: O Render vai colocar seu site no ar em um endereço público.

Vamos começar!

Passo 0: Criando as Pastas e Arquivos (A Receita)
Antes de qualquer coisa, precisamos organizar o projeto no seu computador.

A. Crie a pasta principal:
Em algum lugar do seu computador (como na Área de Trabalho), crie uma nova pasta e dê a ela o nome de crypto_tracker. Todos os arquivos e outras pastas que criarmos ficarão dentro dela.

B. Crie as subpastas:
Agora, dentro da pasta crypto_tracker, crie a seguinte estrutura de subpastas:

Crie uma pasta chamada app.

Dentro da pasta app, crie uma pasta chamada static.

Dentro da pasta static, crie uma pasta chamada js.

Dentro da pasta app, crie também uma pasta chamada templates.

Finalmente, dentro da pasta principal crypto_tracker, crie uma última pasta chamada tests.

No final, sua estrutura de pastas vazias deve parecer assim:

crypto_tracker/
├── app/
│   ├── static/
│   │   └── js/
│   └── templates/
└── tests/

C. Crie cada arquivo e cole o conteúdo:
Agora, vamos criar cada arquivo de texto, um por um. Para cada item abaixo, faça o seguinte:

Vá para a pasta indicada.

Crie um novo arquivo de texto em branco com o nome exato fornecido.

Abra o arquivo e cole dentro dele o conteúdo do bloco de código correspondente que eu enviei no chat.

Arquivos dentro de crypto_tracker/app/
Arquivo: __init__.py

Título no chat: "Inicializador da Aplicação"

O que faz: Inicia e configura a aplicação Flask.

Arquivo: routes.py

Título no chat: "Rotas da Aplicação (Páginas e API)"

O que faz: Define os links do site (ex: a página inicial, a página de detalhes, etc.).

Arquivo: services.py

Título no chat: "Serviço CoinGecko"

O que faz: É o responsável por buscar os dados de preços na internet (na API da CoinGecko).

Arquivo: cache.py

Título no chat: "Configuração do Cache"

O que faz: Guarda os dados de preços por um tempo para não ter que buscá-los toda hora, deixando o site mais rápido.

Arquivo: limiter.py

Título no chat: "Configuração do Rate Limiter"

O que faz: Protege o site contra ataques, limitando o número de acessos que um usuário pode fazer.

Arquivos dentro de crypto_tracker/app/templates/
Arquivo: base.html

Título no chat: "Template Base"

O que faz: É o "esqueleto" de todas as páginas do site (menu, rodapé, etc.).

Arquivo: index.html

Título no chat: "Página Inicial (index.html)"

O que faz: É o visual da página principal, com a tabela de moedas.

Arquivo: coin.html

Título no chat: "Página de Detalhes da Moeda (coin.html)"

O que faz: É o visual da página que mostra os detalhes e o gráfico de uma única moeda.

Arquivo dentro de crypto_tracker/app/static/js/
Arquivo: main.js

Título no chat: "JavaScript do Frontend"

O que faz: Controla toda a interatividade do site, como o gráfico, a busca e a atualização automática de preços.

Arquivo dentro de crypto_tracker/tests/
Arquivo: test_api.py

Título no chat: "Testes da API"

O que faz: Contém testes automáticos para verificar se a API do nosso site está funcionando corretamente.

Arquivos na pasta principal crypto_tracker/
Arquivo: run.py

Título no chat: "Ponto de Entrada da Aplicação"

O que faz: É o arquivo que de fato "liga" o servidor para o site funcionar.

Arquivo: requirements.txt

Título no chat: "Dependências Python"

O que faz: É a lista de "ferramentas" extras que o Python precisa instalar para o projeto rodar.

Arquivo: Dockerfile

Título no chat: "Dockerfile"

O que faz: É uma "receita" para o Docker criar um pacote completo da nossa aplicação.

Arquivo: docker-compose.yml

Título no chat: "Docker Compose"

O que faz: Ajuda a rodar o pacote Docker de forma mais fácil.

Arquivo: .gitignore

Título no chat: "Git Ignore"

O que faz: Diz ao sistema de versionamento (Git) quais arquivos e pastas ele deve ignorar.

Arquivo: LICENSE

Título no chat: "Licença MIT"

O que faz: Define as regras de uso do seu projeto (é um software de código aberto).

Arquivo: CHECKLIST_DE_ACEITACAO.md

Título no chat: "Checklist de Aceitação"

O que faz: Uma lista para você verificar se tudo foi entregue como pedido.

Arquivo: README.md

O que faz: É este próprio arquivo de instruções que você está lendo!

Ufa! Depois de criar todas as pastas e arquivos e colar os conteúdos, você está pronto para os próximos passos.

Passo 1: Enviar o Projeto para o GitHub
Agora que temos todos os arquivos e pastas organizados, vamos colocá-los no GitHub.

Crie uma conta no GitHub: Se ainda não tem, crie uma em github.com.

Crie um novo repositório:

Clique no + no canto superior direito e selecione "New repository".

Dê um nome (ex: crypto-tracker), deixe como Público e clique em "Create repository".

Faça o upload dos arquivos:

Na página do seu repositório, clique em "Add file" > "Upload files".

Arraste a pasta principal crypto_tracker (com tudo dentro) para a área de upload. O GitHub vai carregar todas as pastas e arquivos de uma vez.

Escreva uma mensagem de commit (ex: "Versão inicial do projeto") e clique em "Commit changes".

Passo 2: Publicar o Site com o Render
Crie uma conta no Render:

Acesse render.com e se inscreva usando sua conta do GitHub.

Crie um novo "Web Service":

No painel do Render, clique em "New +" > "Web Service".

Conecte sua conta GitHub e dê permissão para o Render acessar seu repositório crypto_tracker.

Selecione o repositório crypto-tracker na lista e clique em "Connect".

Configure o Serviço Web:

Name: Dê um nome único (ex: meu-crypto-tracker).

Start Command: Apague o que estiver lá e cole isto:

gunicorn run:app

Escolha o Plano Gratuito e clique em "Create Web Service".

Aguarde alguns minutos enquanto o Render constrói e publica seu site.

Passo 3: Acesse seu Site!
No topo da página do Render, você verá a URL do seu site, como https://meu-crypto-tracker.onrender.com. Clique nela!

Parabéns, seu projeto está online e acessível para qualquer pessoa no mundo!
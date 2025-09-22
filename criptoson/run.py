from app import create_app

# Cria a instância da aplicação Flask usando a fábrica.
app = create_app()

if __name__ == '__main__':
    # Roda a aplicação em modo de desenvolvimento.
    # O host '0.0.0.0' torna a aplicação acessível na sua rede local.
    app.run(host='0.0.0.0', port=5000, debug=True)

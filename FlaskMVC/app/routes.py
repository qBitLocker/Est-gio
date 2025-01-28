from mvc_flask import Router

# 1º Parâmetro: Interface Web
# 2º Parâmetro: home#index (Home - Nome do Controller e index é a action (Método do controller))
Router.get('/', 'home#index')

# Para acessar a rota => controllers/{controller_name}_controller.py
Router.get('/product', 'posts#show')
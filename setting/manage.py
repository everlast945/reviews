from wsgiref import simple_server

from setting.wsgi import app

# Создаем сервер (локально)
server = simple_server.WSGIServer(('127.0.0.1', 8000), simple_server.WSGIRequestHandler)
# Задаем приложение (микросервис)
server.set_app(app)
# Запуск сервера
server.serve_forever()
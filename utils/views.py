import os
import json
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader

from utils.utils import RequestMethods


class BaseView:
    template = None

    def __init__(self, env, response_method, request_method, args) -> None:
        super().__init__()
        self.env = env
        self.response_method = response_method
        self.request_method = request_method
        self.post_data = self._get_post_data()
        self.args = args

    def dispatch(self):
        """
        Отправка
        """
        # Определяем тип запроса. Если метод GET то вызывается метод self.get()
        method = getattr(self, RequestMethods.METHODS.get(self.request_method), None)
        if method:
            return method()
        return self.method_not_allowed()

    def method_not_allowed(self):
        """
        Ошибка. Метод не поддерживается представлением
        """
        self.response_method('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [f'Метод {self.request_method}. Не поддерживается.'.encode('utf-8')]

    def _response_200(self):
        self.response_method('200 OK', [('Content-Type', 'text/html')])

    def _get_post_data(self):
        """
        Приведение пост ответа к нормальному виду
        """
        input = self.env['wsgi.input']
        lenght = int(self.env.get('CONTENT_LENGTH')) if self.env.get('CONTENT_LENGTH') else 0
        data = input.read(lenght).decode() if lenght > 0 else '{}'
        return parse_qs(data)

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update(dict(
            static_path=os.environ.get('STATIC_PATH'),
        ))
        return context

    def _render(self, **kwargs):
        templates_path = os.environ.get('TEMPLATES_PATH')
        template = Environment(loader=FileSystemLoader(templates_path)).get_template(self.template)
        return [template.render(self.get_context_data(**kwargs)).encode('utf-8')]

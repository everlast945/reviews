import re
import os
from wsgiref import simple_server

SETTING_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(SETTING_DIR)
os.environ['STATIC_PATH'] = os.path.join(BASE_DIR, 'assets')
os.environ['TEMPLATES_PATH'] = os.path.join(BASE_DIR, 'templates')


def set_env(file_path) -> None:
    """
    Перенос параметров из файла в виртуальное окружение (написал своё т.к. нельзя испольовать другие пакеты)
    :param file_path: Путь к файлу с параметрами
    """
    env_pattern = re.compile("(\w+)(?:=)(.*)$", re.MULTILINE)
    with open(file_path, "r") as env_file:
        env_text = env_file.read()
        env_match_list = re.findall(env_pattern, env_text)
        for env_match in env_match_list:
            os.environ[env_match[0]] = env_match[1]


set_env(os.path.join(SETTING_DIR, '.env_local'))


# region wsgi server


def app(env, response_method):
    path = env.get('PATH_INFO', '').lstrip('/')
    method = env.get('REQUEST_METHOD')

    from setting.urls import urls
    for regex, class_view in urls:
        match = re.search(regex, path)
        if match is not None:
            args = match.groups()
            view = class_view(env, response_method, method, args)
            response = view.dispatch()
            if response:
                return response

    response_method('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Page Not Found.'.encode('utf-8')]


server = simple_server.WSGIServer(('127.0.0.1', 8000), simple_server.WSGIRequestHandler)
server.set_app(app)
server.serve_forever()
# endregion
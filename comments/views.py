
from utils.views import BaseView
from setting.database import DBManager


class CommentCreateListView(BaseView):
    template = 'comments/list.j2'

    def get(self):
        cursor = DBManager().db_cursor()
        sql = f'SELECT * FROM comments'
        cursor.execute(sql)
        comments = cursor.fetchall()
        self._response_200()
        return self._render(comments=comments)

    def post(self):
        self._response_200()
        return [f'Comment CREATE {self.post_data}'.encode('utf-8')]


class CommentDetailUpdateDeleteView(BaseView):
    template = 'list.j2'

    def get(self):
        self._response_200()
        return ['Comment DETAIL'.encode('utf-8'), 'Comment DETAIL'.encode('utf-8')]

    def put(self):
        self._response_200()
        return ['Comment UPDATE'.encode('utf-8')]

    def delete(self):
        self._response_200()
        return ['Comment DELETE'.encode('utf-8')]

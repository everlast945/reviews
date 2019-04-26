from setting.database import DBManager
from utils.views import BaseView


class CommentListView(BaseView):
    template = 'comments/list.j2'

    def get(self):
        table_name = 'comments ' \
                     'LEFT JOIN regions ' \
                     'ON comments.region_id = regions.id ' \
                     'LEFT JOIN cities ' \
                     'ON comments.city_id = cities.id'
        comments = DBManager().select(table_name=table_name)
        self._response_200()
        return self._render(comments=comments)


class CommentCreateView(BaseView):
    template = 'comments/create.j2'

    def get(self):
        regions = DBManager().select(table_name='regions')
        self._response_200()
        return self._render(regions=regions)

    def post(self):
        fields = ['first_name', 'second_name', 'last_name', 'region_id', 'city_id', 'phone', 'email', 'text']
        values = [f"'{self.post_data.get(field, [' '])[0]}'" for field in fields]
        DBManager().create('comments', fields, values)
        # self._response_200()
        self.response_method('301 Moved Permanently', [('Location', '/comments/')])
        return self._render()


class CommentDeleteView(BaseView):

    def delete(self):
        DBManager().delete('comments', f'id = {self.args[0]}')
        self._response_200()
        return ['Comment DELETE'.encode('utf-8')]






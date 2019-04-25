from setting.database import DBManager
from utils.views import BaseView


class StatListView(BaseView):
    template = 'regions/region_by_many_comments.j2'

    def get(self):
        sql = "SELECT regions.*, COUNT(comments.region_id) as comments_count " \
              "FROM regions " \
              "LEFT JOIN comments " \
              "ON regions.id = comments.region_id " \
              "GROUP BY regions.id, regions.name " \
              "HAVING comments_count > 5 " \
              "ORDER BY -comments_count"
        regions = DBManager().run(sql)
        self._response_200()
        return self._render(regions=regions)

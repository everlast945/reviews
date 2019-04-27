from setting.database import DBManager
from utils.views import BaseView


class CitiesByRegionListView(BaseView):
    template = 'cities/list_by_region.j2'

    def get(self):
        sql = f"SELECT cities.*, COUNT(comments.city_id) as comments_count " \
            f"FROM cities " \
            f"LEFT JOIN comments " \
            f"ON cities.id = comments.city_id " \
            f"GROUP BY cities.id, cities.name " \
            f"HAVING cities.region_id = {self.args[0]} " \
            f"ORDER BY -comments_count"
        cities = DBManager().run(sql)
        self._response_200()
        return self._render(cities=cities)


class CitiesChoiceAjaxView(BaseView):
    template = '_fields/_select_field.j2'

    def get(self):
        self._response_200()
        filter = f'region_id = {self.args[0]}'
        cities = DBManager().select(table_name='cities', filter=filter)
        return self._render(values=cities, label='Город', name='city_id')

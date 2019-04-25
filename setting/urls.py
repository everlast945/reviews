from cities.views import CitiesChoiceAjaxView, CitiesByRegionListView
from comments.views import CommentListView, CommentDeleteView, CommentCreateView

# Роутинг к контроллерам
from regions.views import StatListView

# todo: Раскидать роутинг. И заменить на инклуды
urls = [
    (r'^$', CommentListView),

    (r'^comments/$', CommentListView),
    (r'^comments/create/$', CommentCreateView),
    (r'^comments/(\d+)/$', CommentDeleteView),

    (r'^cities/choices/ajax/(\d+)/$', CitiesChoiceAjaxView),

    (r'^regions/$', StatListView),
    (r'^cities/by_region/(\d+)/$', CitiesByRegionListView),
]

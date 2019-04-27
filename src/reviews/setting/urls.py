from regions.comments.views import CommentListView
from regions.urls import urls as regions_urls
from regions.comments.urls import urls as regions_comments_urls
from regions.cities.urls import urls as regions_cities_urls

urls = [
    (r'^$', CommentListView),
] \
       + regions_urls \
       + regions_comments_urls \
       + regions_cities_urls

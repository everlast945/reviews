from .views import CommentListView, CommentDeleteView, CommentCreateView

urls = [
    (r'^regions/comments/$', CommentListView),
    (r'^regions/comments/create/$', CommentCreateView),
    (r'^regions/comments/(\d+)/$', CommentDeleteView),
]

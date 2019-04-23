from comments.views import CommentCreateListView, CommentDetailUpdateDeleteView

urls = [
    (r'^comments/$', CommentCreateListView),
    (r'^comments/(\d+)/$', CommentDetailUpdateDeleteView),
]

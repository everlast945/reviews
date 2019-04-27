from .views import CitiesChoiceAjaxView, CitiesByRegionListView

urls = [
    (r'^regions/cities/choices/ajax/(\d+)/$', CitiesChoiceAjaxView),
    (r'^regions/cities/by_region/(\d+)/$', CitiesByRegionListView),
]

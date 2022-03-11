from django.urls import path
from body.views.home import HomeView

HOME_INDEX_ROUTE = "index"

urlpatterns = [
    path("", HomeView.as_view(), name=HOME_INDEX_ROUTE),
]

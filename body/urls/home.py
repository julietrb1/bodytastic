from django.urls import path
from body.views.home_views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
]

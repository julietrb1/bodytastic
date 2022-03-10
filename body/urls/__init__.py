from django.urls import include, path

urlpatterns = [
    path("body/", include("body.urls.mybody")),
    path("medication/", include("body.urls.medication")),
    path("mind-and-soul/", include("body.urls.mind_and_soul")),
    path("life-events/", include("body.urls.life_events")),
    path("", include("body.urls.home")),
]

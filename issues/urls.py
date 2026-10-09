
from django.urls import path
from .views import reporters_api, issues_api

urlpatterns = [
    path("reporters/", reporters_api, name="reporters_api"),
    path("issues/", issues_api, name="issues_api"),
]

from django.urls.conf import re_path
from api.views import PortifolioView
from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    re_path(r'trades/lucro/?$', PortifolioView.as_view(), name="lucro"),
]

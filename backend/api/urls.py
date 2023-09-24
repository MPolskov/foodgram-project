from django.urls import path, include
from rest_framework import routers

app_name = 'api'


router = routers.DefaultRouter()
# router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

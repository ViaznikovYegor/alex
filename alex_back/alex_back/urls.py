from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path

from api import views

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
]

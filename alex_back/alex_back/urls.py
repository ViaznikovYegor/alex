from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path

from api import views

router = DefaultRouter()
router.register(r'artists', views.ArtistViewSet, basename='artist')
router.register(r'me/artists', views.ArtistLikeViewSet, basename='artists')
router.register(r'releases', views.ReleaseViewSet, basename='realese')
router.register(r'me/releases', views.ReleaseLikeViewSet, basename='realeses')
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'songs', views.SongViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
]

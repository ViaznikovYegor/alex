from rest_framework import viewsets
from rest_framework import mixins
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Value, BooleanField, Exists, OuterRef, Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ArtistSerializer,
    ReleaseSerializer,
    PlaylistSerializer,
    PlaylistListSerializer,
    ArtistLikeSerializer,
    SongLikeSerializer,
    ToggleLikeSerializer,
    ReleaseFullSerializer,
    ReleaseLikeSerializer
)
from .models import (
    Artist,
    Release,
    Playlist,
    Song,
    LikedArtist,
    LikedRelease
)


@extend_schema_view(
    like=extend_schema(
        summary="Лайк / дизлайк артиста",
        request=ToggleLikeSerializer,
        responses={
            200: None,
            204: None,
        },
    )
)
class ArtistViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        user = self.request.user
        return Artist.objects.annotate(
            listeners=Sum('song__listenings'),
            is_liked=Exists(
                LikedArtist.objects.filter(
                    user=user,
                    artists=OuterRef('pk')
                )
            ) if getattr(user, 'is_authenticated', False) else False
        )

    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        if request.method == 'POST':
            serializer = ToggleLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            is_liked = serializer.validated_data['is_liked']

            if is_liked:
                LikedArtist.objects.get_or_create(
                    user=request.user,
                    artists_id=pk
                )
            else:
                LikedArtist.objects.filter(
                    user=request.user,
                    artists_id=pk
                ).delete()

            return Response(status=status.HTTP_200_OK)

        # DELETE
        LikedArtist.objects.filter(
            user=request.user,
            artists_id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtistLikeViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = ArtistLikeSerializer

    def get_queryset(self):
        return Artist.objects.filter(liked_artist__user=self.request.user)


class ReleaseLikeViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReleaseLikeSerializer
    def get_queryset(self):
        return Release.objects.filter(liked_release__user=self.request.user)


@extend_schema_view(
    like=extend_schema(
        summary="Лайк / дизлайк",
        request=ToggleLikeSerializer,
        responses={
            200: None,
            204: None,
        },
    )
)
class ReleaseViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    def get_serializer_class(self):
        if self.action == 'list':
            return ReleaseSerializer
        return ReleaseFullSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Release.objects.all()
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_liked=Exists(LikedRelease.objects.filter(user=user, releases=OuterRef('pk')))
            )
        else:
            queryset = queryset.annotate(is_liked=Value(False, output_field=BooleanField()))
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        if request.method == 'POST':
            serializer = ToggleLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            is_liked = serializer.validated_data['is_liked']

            if is_liked:
                LikedRelease.objects.get_or_create(
                    user=request.user,
                    releases_id=pk
                )
            else:
                LikedRelease.objects.filter(
                    user=request.user,
                    releases_id=pk
                ).delete()

            return Response(status=status.HTTP_200_OK)

        # DELETE
        LikedRelease.objects.filter(
            user=request.user,
            releases_id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongLikeSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistListSerializer

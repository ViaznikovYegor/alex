from rest_framework import serializers

from .models import (
    Artist,
    Release,
    Playlist,
    Song,
    LikedSong,
    LikedArtist,
    LikedRelease
)


class ReleaseArtistSerializer(serializers.ModelSerializer):
    artists = serializers.StringRelatedField(read_only=True, many=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'cover',
            'type',
            'artists',
            'is_liked'
        )
        model = Release


class SongArtistSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    artists = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'artists',
            'is_liked',
            'position',
            'disk'
        )
        model = Song

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            has_like = LikedSong.objects.filter(
                user=request.user,
                songs=obj
            ).exists()
            return bool(has_like)
        return 0


class SongLikeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Song


class PlaylistListSerializer(serializers.ModelSerializer):
    cover = serializers.StringRelatedField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'cover',
            'count'
        )
        model = Playlist


class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Playlist


class ArtistSerializer(serializers.ModelSerializer):
    releases = ReleaseArtistSerializer(read_only=True, many=True)
    songs = SongArtistSerializer(read_only=True, many=True)
    listeners = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    covers = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'covers',
            'bio',
            'releases',
            'songs',
            'listeners',
            'is_liked'
        )
        model = Artist


class ArtistLikeSerializer(serializers.ModelSerializer):
    covers = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'covers'
        )
        model = Artist


class ReleaseLikeSerializer(serializers.ModelSerializer):
    artists = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'cover',
            'type',
            'artists'
        )
        model = Release


class LikedArtistSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'is_liked', 'artist', 'user')
        model = LikedArtist


class ReleaseFullSerializer(serializers.ModelSerializer):
    artists = ArtistLikeSerializer(read_only=True, many=True)
    songs = SongArtistSerializer(source='song_set', read_only=True, many=True)  # если не менял модель
    is_liked = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'cover', 'type', 'artists', 'songs', 'is_liked')
        model = Release

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LikedRelease.objects.filter(user=request.user, releases=obj).exists()
        return False


class ReleaseSerializer(serializers.ModelSerializer):
    artists = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'cover',
            'type',
            'artists'
        )
        model = Release


class ToggleLikeSerializer(serializers.Serializer):
    """Простой сериализатор только для лайка артиста"""
    is_liked = serializers.BooleanField(required=True)

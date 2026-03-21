from rest_framework import serializers


from .models import (
    User,
    Artist,
    Release,
    Playlist,
    Song, 
    LikedSong,
    SongRelease,
    SongPlaylist,
    UserSearch,
    UserHistory
)


class User(serializers.ModelSerializer):

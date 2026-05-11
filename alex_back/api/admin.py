from django.contrib import admin
from .models import (
    Mood, Genre, Cover, Artist, Release, Playlist, Song,
    LikedSong, LikedArtist, LikedRelease, SongRelease, SongPlaylist,
    UserSearch, UserHistory
)


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('id', 'cover')
    # Если нужно показывать превью, можно добавить метод


class LikedSongInline(admin.TabularInline):
    model = LikedSong
    extra = 1
    raw_id_fields = ('user',)


class SongReleaseInline(admin.TabularInline):
    model = SongRelease
    extra = 1
    raw_id_fields = ('release',)
    fields = ('release', 'order')


class SongPlaylistInline(admin.TabularInline):
    model = SongPlaylist
    extra = 1
    raw_id_fields = ('playlist',)
    fields = ('playlist', 'order')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listenings', 'listenings_last_week', 'disk', 'position')
    list_filter = ('moods', 'genres', 'artists', 'release')
    search_fields = ('name',)
    filter_horizontal = ('moods', 'genres', 'artists', 'release', 'playlist')
    inlines = [LikedSongInline, SongReleaseInline, SongPlaylistInline]
    # Обратите внимание: поле 'users' с through='LikedSong' не может использовать filter_horizontal,
    # для него используется inline LikedSongInline


class LikedArtistInline(admin.TabularInline):
    model = LikedArtist
    extra = 1
    raw_id_fields = ('user',)


class ArtistCoverInline(admin.TabularInline):
    model = Artist.covers.through
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('users', 'covers')
    inlines = [LikedArtistInline]
    prepopulated_fields = {'links': ('name',)}  # если links это SlugField


class LikedReleaseInline(admin.TabularInline):
    model = LikedRelease
    extra = 1
    raw_id_fields = ('user',)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'type')
    list_filter = ('type', 'date', 'artists')
    search_fields = ('name',)
    filter_horizontal = ('artists', 'users')
    inlines = [LikedReleaseInline]


class SongPlaylistInlineForPlaylist(admin.TabularInline):
    model = SongPlaylist
    extra = 1
    raw_id_fields = ('songs',)
    fields = ('songs', 'order')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('author_users', 'liked_users')
    inlines = [SongPlaylistInlineForPlaylist]


@admin.register(LikedSong)
class LikedSongAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'songs', 'is_liked')
    list_filter = ('is_liked',)
    search_fields = ('user__username', 'songs__name')
    raw_id_fields = ('user', 'songs')


@admin.register(LikedArtist)
class LikedArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'artists', 'is_liked')
    list_filter = ('is_liked',)
    search_fields = ('user__username', 'artists__name')
    raw_id_fields = ('user', 'artists')


@admin.register(LikedRelease)
class LikedReleaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'releases', 'is_liked')
    list_filter = ('is_liked',)
    search_fields = ('user__username', 'releases__name')
    raw_id_fields = ('user', 'releases')


@admin.register(SongRelease)
class SongReleaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'release', 'songs', 'order')
    list_filter = ('release',)
    search_fields = ('songs__name', 'release__name')
    raw_id_fields = ('songs', 'release')


@admin.register(SongPlaylist)
class SongPlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'playlist', 'songs', 'order')
    list_filter = ('playlist',)
    search_fields = ('songs__name', 'playlist__name')
    raw_id_fields = ('songs', 'playlist')


@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)
    filter_horizontal = ('users',)


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'time')
    list_filter = ('time',)
    filter_horizontal = ('users', 'songs')
    date_hierarchy = 'time'
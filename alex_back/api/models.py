from django.db import models
from django.contrib.auth.models import User


class Mood(models.Model):
    name = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = 'Настроение'
        verbose_name_plural = 'Настроения'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField('Имя', max_length=50)
    bio = models.TextField('Биография', blank=True)
    links = models.SlugField('Ссылки', blank=True)
    users = models.ManyToManyField(User, verbose_name='Пользователи', blank=True)

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.name


class Release(models.Model):
    class ReleaseType(models.TextChoices):
        EP = 'EP', 'ЕР'
        ALBUM = 'ALBUM', 'Альбом'
        SINGLE = 'SINGLE', 'Сингл'

    name = models.CharField('Название', max_length=50)
    cover = models.ImageField('Обложка', upload_to='releases/')
    date = models.DateField('Дата выпуска')
    release_type = models.CharField(
        'Тип релиза',
        max_length=10,
        choices=ReleaseType.choices,
        default=ReleaseType.SINGLE,
    )
    artists = models.ManyToManyField(Artist, verbose_name='Исполнители')
    users = models.ManyToManyField(User, verbose_name='Пользователи', blank=True)

    class Meta:
        verbose_name = 'Релиз'
        verbose_name_plural = 'Релизы'

    def __str__(self):
        return f'{self.name} ({self.get_release_type_display()})'


class Playlist(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    author_users = models.ManyToManyField(User, verbose_name='Авторы', related_name='authored_playlists')
    liked_users = models.ManyToManyField(User, verbose_name='Лайкнувшие', blank=True, related_name='liked_playlists')

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField('Название', max_length=100)
    listenings = models.IntegerField('Прослушиваний')
    listenings_last_week = models.IntegerField('Прослушиваний за неделю')
    path = models.SlugField('Путь к файлу')
    # Связи
    moods = models.ManyToManyField(Mood, verbose_name='Настроения')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    artists = models.ManyToManyField(Artist, verbose_name='Исполнители')
    release = models.ManyToManyField(Release, verbose_name='Релизы')
    playlist = models.ManyToManyField(Playlist, verbose_name='Плейлисты', blank=True)
    users = models.ManyToManyField(
        User,
        through='LikedSong',
        verbose_name='Лайкнувшие пользователи',
        blank=True
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def __str__(self):
        return self.name


class LikedSong(models.Model):
    songs = models.ForeignKey(Song, verbose_name='Песня', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_liked = models.BooleanField('Лайк', default=True)

    class Meta:
        verbose_name = 'Лайкнутая песня'
        verbose_name_plural = 'Лайкнутые песни'
        unique_together = ('songs', 'user')

    def __str__(self):
        return f'{self.user} – {self.songs} ({self.is_liked})'


class SongRelease(models.Model):
    songs = models.ForeignKey(Song, verbose_name='Песня', on_delete=models.CASCADE)
    release = models.ForeignKey(Release, verbose_name='Релиз', on_delete=models.CASCADE)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Порядок в релизе'
        verbose_name_plural = 'Порядок в релизе'
        unique_together = ('songs', 'release')

    def __str__(self):
        return f'{self.release} – {self.songs} ({self.order})'


class SongPlaylist(models.Model):
    songs = models.ForeignKey(Song, verbose_name='Песня', on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, verbose_name='Плейлист', on_delete=models.CASCADE)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Порядок в плейлисте'
        verbose_name_plural = 'Порядок в плейлисте'
        unique_together = ('songs', 'playlist')

    def __str__(self):
        return f'{self.playlist} – {self.songs} ({self.order})'


class UserSearch(models.Model):
    text = models.TextField('Текст запроса')
    users = models.ManyToManyField(User, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'Поисковые запросы'

    def __str__(self):
        return self.text[:50]


class UserHistory(models.Model):
    time = models.DateTimeField('Время прослушивания')
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    songs = models.ManyToManyField(Song, verbose_name='Песни')

    class Meta:
        verbose_name = 'История прослушиваний'
        verbose_name_plural = 'Истории прослушиваний'

    def __str__(self):
        times = self.time.strftime('%d.%m.%Y %H:%M')
        return f'История на {times}'

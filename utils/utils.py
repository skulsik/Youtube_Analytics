import os
import json
import isodate
import datetime
from googleapiclient.discovery import build


class InitAPIYouTube:
    # API_You_Tube_KEY скопирован из гугла и вставлен в переменные окружения, далее присвоен переменной
    name_of_the_environment_variable = 'API_You_Tube_KEY'


    def __init__(self, name_key: str = name_of_the_environment_variable):
        """
        Создает и возвращает объект для работы с API
        :param name_key: Либо получаем имя ключа, либо присваиваем по умолчанию из переменной
        """
        # Получает сам ключ, из переменных окружения Windows
        if os.getenv(name_key):
            api_key: str = os.getenv(name_key)
        else:
            raise ValueError('В переменных окружения Windows отсутствует ключ api youtube.')

        # создает специальный объект для работы с API
        self.youtube_object: object = build('youtube', 'v3', developerKey=api_key)


    def get_object_youtube(self) -> object:
        """
        :return: Возвращает объект с youtube API
        """
        return self.youtube_object


class Channel(InitAPIYouTube):
    def __init__(self, channel_id: str):
        """
        Инициализация атрибутов, считывание инфо о канале
        :param channel_id: id канала
        """
        # Создает и возвращает объект для работы с API
        super().__init__()

        # Читаем инфо по id в словарь
        self.channel: dict = self.get_object_youtube().channels().list(id=channel_id, part='snippet,statistics').execute()

        # Инициализация переменных
        # Id канала
        self.__channel_id: str = channel_id

        # Имя канала
        self.channel_name: str = self.channel["items"][0]["snippet"]["title"]

        # Описание канала
        self.channel_description: str = self.channel["items"][0]["snippet"]["description"]

        # Ссылка на канал
        self.channel_link: str = self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]

        # Количество подписчиков
        self.number_of_subscriber = self.channel["items"][0]["statistics"]["subscriberCount"]

        # Количество видео
        self.number_of_video = self.channel["items"][0]["statistics"]["videoCount"]

        # Количество просмотров
        self.number_of_views = self.channel["items"][0]["statistics"]["viewCount"]


    @property
    def channel_id(self) -> str:
        """
        Доступ к переменной
        :return:
        """
        return self.__channel_id


    def print_info(self, json_unordered: dict) -> dict:
        """
        Возврат инфы в формате json
        :return:
        """
        return json.dumps(json_unordered, indent=2, ensure_ascii=False)


    def to_json(self):
        """
        Запись json фаила на диск, json берется с текущего канала
        :return:
        """
        # Путь директории для записи json файла
        path = f"json\{self.channel_name}.json"
        with open(path, "w") as file:
            json.dump(self.print_info(self.channel), file)


    def __str__(self) -> str:
        """
        :return: Возврат название канала
        """
        return f"YouTube канал: {self.channel_name}"


    def __gt__(self, other) -> bool:
        """
        :param other: Другой экземпляр
        :return: Возврат результата сравнения
        """
        return self.number_of_subscriber > other.number_of_subscriber


    def __lt__(self, other) -> bool:
        """
        :param other: Другой экземпляр
        :return: Возврат результата сравнения
        """
        return self.number_of_subscriber < other.number_of_subscriber


    def __add__(self, other) -> int:
        """
        :param other: Другой экземпляр
        :return: Возврат сцммы количенства подписчиков двух экземпляров
        """
        return self.number_of_subscriber + other.number_of_subscriber


class Video(InitAPIYouTube):
    def __init__(self, video_id: str = None):
        """
        Считывает с YouTube информацию о видео. Инициализирует переменные.
        :param video_id: Id видео
        """
        # Инициализация переменных
        # Хранение ошибки для передачи в тесты
        self.Error_YouTube: object = None

        # Название видео
        self.video_name: str = None

        # Количество просмотров
        self.number_of_views: str = None

        # Количество лайков
        self.number_of_likes: str = None

        # Создает и возвращает объект для работы с API
        super().__init__()

        try:
            # Читаем инфо по id в список
            self.video: dict = self.get_object_youtube().videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()

            if self.video['items']:
                self.video_name = self.video["items"][0]["snippet"]["title"]
                self.number_of_views = self.video["items"][0]["statistics"]["viewCount"]
                self.number_of_likes = self.video["items"][0]["statistics"]["likeCount"]
            else:
                raise VideoIdError('VideoIdError: Проверьте правильность введеного Id')
        except VideoIdError as e:
            self.Error_YouTube = e


    def __str__(self) -> str:
        """
        :return: Возврат название видео
        """
        return f"Название видео: {self.video_name}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        """
        Считывает с YouTube информацию о плайлисте. Инициализирует переменную playlist_name
        :param playlist_id: Id видео
        """
        super().__init__(video_id)

        # Читаем инфо по id в список
        self.playlist: dict = self.get_object_youtube().playlists().list(id=playlist_id, part='snippet').execute()

        # Название плайлиста
        self.playlist_name: str = self.playlist["items"][0]["snippet"]["title"]


    def __str__(self) -> str:
        """
        :return: Возврат название видео и название плайлиста
        """
        return f"Название видео: {self.video_name}. Название плайлиста: {self.playlist_name}."


class PlayList(InitAPIYouTube):
    def __init__(self, playlist_id: str):
        """Инициализация переменных"""
        super().__init__()
        # Читаем инфо по id в список
        self.playlist = self.get_object_youtube().playlists().list(id=playlist_id, part='contentDetails,snippet').execute()
        self.playlist_id: str = playlist_id

        # Название плайлиста
        self.__name_play_list: str = self.playlist["items"][0]["snippet"]["title"]

        # URL плайлиста
        self.__url_of_play_list: str = f'https://www.youtube.com/playlist?list={playlist_id}'


    @property
    def name_play_list(self) -> str:
        """Вывод названия плайлиста"""
        print(self.__name_play_list)
        return self.__name_play_list


    @property
    def url_of_play_list(self) -> str:
        """Вывод url плайлиста"""
        print(self.__url_of_play_list)
        return self.__url_of_play_list


    @property
    def summ_time_of_play_list(self) -> object:
        """
        Складывает продолжительность всех видео
        :return: объект datatime, общая продолжительность всех видео в плэйлисте
        """
        # Читаем инфо по id в список
        playlist: dict = self.get_object_youtube().playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()

        # Создает список id видео из плайлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]

        # Создает список из видео и инфо о них
        video_response: list = self.get_object_youtube().videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

        # Задаем объект datetime
        self.summ_duration: object = datetime.timedelta()

        for video in video_response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration: str = video['contentDetails']['duration']

            # Str -> date, преобразует строку в формат дата
            duration: object = isodate.parse_duration(iso_8601_duration)

            # Сумма длительности всех видео
            self.summ_duration += duration
        return self.summ_duration


    def show_best_video(self):
        """ Поиск видео с максимальным количеством лайков и вывод его url"""
        max_likes: int = 0
        # Читаем инфо по id в список
        for video_id in self.video_ids:
            # Читает инфо о видео
            video: dict = self.get_object_youtube().videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()

            # Количество лайков данного видео
            likes: int = int(video['items'][0]['statistics']['likeCount'])

            # Ищет максимально количество лайков, присваивает url (с максимальным кол-м лайков) в переменную
            if likes > max_likes:
                max_likes = likes
                url_of_max_likes: str = f'https://youtu.be/{video_id}'
        print(url_of_max_likes)
        return url_of_max_likes


    def __str__(self) -> str:
        """
        :return: Возврат название плайлиста
        """
        return f"Название плайлиста: {self.playlist_name}."


class VideoIdError(Exception):
    def __init__(self, *args, **kwarg):
        self.message = args[0] if args else 'VideoIdError: Неизвестная ошибка Id'
        print(self.message)


    def __str__(self):
        return self.message

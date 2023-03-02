import os
import json
from googleapiclient.discovery import build


class InitAPIYouTube:
    # API_You_Tube_KEY скопирован из гугла и вставлен в переменные окружения, далее присвоен переменной
    name_of_the_environment_variable = 'API_You_Tube_KEY'


    def add_object_youtube(self, name_key: str = name_of_the_environment_variable):
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
        self.add_object_youtube()

        # Читаем инфо по id в список
        self.channel = self.get_object_youtube().channels().list(id=channel_id, part='snippet,statistics').execute()

        # Инициализация переменных
        # Id канала
        self.__channel_id = channel_id

        # Имя канала
        self.channel_name = self.channel["items"][0]["snippet"]["title"]

        # Описание канала
        self.channel_description = self.channel["items"][0]["snippet"]["description"]

        # Ссылка на канал
        self.channel_link = self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]

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


class Video(Channel):
    def __init__(self, video_id: str = None):
        """
        Считывает с YouTube информацию о видео. Инициализирует переменные.
        :param video_id: Id видео
        """
        # Создает и возвращает объект для работы с API
        self.add_object_youtube()

        # Читаем инфо по id в список
        self.video = self.get_object_youtube().videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()

        # Инициализация переменных
        # Название видео
        self.video_name = self.video["items"][0]["snippet"]["title"]

        # Количество просмотров
        self.number_of_views = self.video["items"][0]["statistics"]["viewCount"]

        # Количество лайков
        self.number_of_likes = self.video["items"][0]["statistics"]["likeCount"]


    def __str__(self) -> str:
        """
        :return: Возврат название видео
        """
        return f"Название видео: {self.video_name}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """
        Считывает с YouTube информацию о плайлисте. Инициализирует переменную playlist_name
        :param playlist_id: Id видео
        """
        super().__init__(video_id)

        # Читаем инфо по id в список
        self.playlist = self.get_object_youtube().playlists().list(id=playlist_id, part='snippet').execute()

        # Название плайлиста
        self.playlist_name = self.playlist["items"][0]["snippet"]["title"]


    def __str__(self) -> str:
        """
        :return: Возврат название видео и название плайлиста
        """
        return f"Название видео: {self.video_name}. Название плайлиста: {self.playlist_name}."

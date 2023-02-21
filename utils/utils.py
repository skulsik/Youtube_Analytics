import os, json
from googleapiclient.discovery import build


class InitAPIYouTube:
    # API_You_Tube_KEY скопирован из гугла и вставлен в переменные окружения, далее присвоен переменной
    name_of_the_environment_variable = 'API_You_Tube_KEY'


    def add_object_youtube(self, name_key=name_of_the_environment_variable):
        """
        Создает и возвращает объект для работы с API
        :param name_key: Либо получаем имя ключа, либо присваиваем по умолчанию из переменной
        """
        # Получает сам ключ, из переменных окружения Windows
        api_key: str = os.getenv(name_key)
        # создает специальный объект для работы с API
        self.youtube_object = build('youtube', 'v3', developerKey=api_key)


    def get_object_youtube(self):
        """
        :return: Возвращает объект с youtube API
        """
        return self.youtube_object


class Channel(InitAPIYouTube):
    def __init__(self, channel_id):
        """
        Инициализация атрибутов, считывание инфо о канале
        :param channel_id: id канала
        """
        # Создает и возвращает объект для работы с API
        self.add_object_youtube()

        # Читаем инфо по id в список
        self.channel = self.get_object_youtube().channels().list(id=channel_id, part='snippet,statistics').execute()

        # Инициализация переменных
        self.__channel_id = channel_id
        self.channel_name = self.channel["items"][0]["snippet"]["title"]
        self.channel_description = self.channel["items"][0]["snippet"]["description"]
        self.channel_link = self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.number_of_subscriber = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.number_of_video = self.channel["items"][0]["statistics"]["videoCount"]
        self.number_of_views = self.channel["items"][0]["statistics"]["viewCount"]


    @property
    def channel_id(self):
        """
        Доступ к переменной
        :return:
        """
        return self.__channel_id


    def print_info(self) -> dict:
        """
        Возврат инфы в формате json
        :return:
        """
        return json.dumps(self.channel, indent=2, ensure_ascii=False)


    def to_json(self):
        """
        Запись json фаила на диск, json берется с текущего канала
        :return:
        """
        # Путь директории для записи json файла
        path = f"json\{self.channel_name}.json"
        with open(path, "w") as file:
            json.dump(self.print_info(), file)

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
        self.youtube = build('youtube', 'v3', developerKey=api_key)


class Channel(InitAPIYouTube):
    def read_info(self, channel_id):
        """
        Читаем инфо по id в список
        :param channel_id: id канала
        :return: список информации
        """
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return self.channel


    def print_info(self):
        """
        Вывод инфы в формате json
        :return:
        """
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

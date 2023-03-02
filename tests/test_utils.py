from utils.utils import *
import json
import pytest


class Test_InitAPIYouTube():
    # Создаем экземпляр для теста
    object_youtube = InitAPIYouTube()


    def test_add_object_youtube_api_key_error(self):
        """
        Проверка c неверно введеным ключем, либо ключ отсутствует в переменных окружениях
        :return:
        """
        with pytest.raises(ValueError, match='В переменных окружения Windows отсутствует ключ api youtube.'):
            self.object_youtube.add_object_youtube('This_my_key')


    def test_add_object_youtube_not_error(self):
        """
        Проверка c верно введеным ключем
        :return: None в случае создания объекта, иначе ошибка!!!
        """
        assert self.object_youtube.add_object_youtube() == None


    def test_get_object_youtube_not_error(self):
        """
        Объект существует
        :return:
        """
        self.object_youtube.add_object_youtube()
        assert self.object_youtube.get_object_youtube() != None


class Test_Channel():
    # Создаем экземпляр для теста
    object_channel = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")


    def test_channel_id(self):
        """
        Проверка с существующим id
        :return:
        """
        assert self.object_channel.channel_id == "UCMCgOm8GZkHp8zJ6l7_hIuA"

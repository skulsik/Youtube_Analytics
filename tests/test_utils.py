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


class Test_Video():
    def test_video_no_id(self):
        """Проверка с несуществующим id"""
        video = Video('broken_video_id')
        assert str(video.Error_YouTube) == 'VideoIdError: Проверьте правильность введеного Id'


    def test_video_id(self):
        """Проверка с существующим id"""
        video = Video('9lO06Zxhu88')
        assert video.Error_YouTube == None


class Test_PLVideo():
    def test_PL_video(self):
        """Проверка на вывод корректных данных"""
        video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
        assert str(video2) == 'Название видео: Пушкин: наше все?. Название плайлиста: Литература.'


class Test_PlayList():
    def test_name_play_list(self):
        """Проверка на вывод корректных данных"""
        pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
        assert pl.name_play_list == 'Редакция. АнтиТревел'


    def test_url_of_play_list(self):
        """Проверка на вывод корректных данных"""
        pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
        assert pl.url_of_play_list == 'https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb'


    def test_summ_time_of_play_list(self):
        """Проверка на вывод корректных данных"""
        pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
        duration = pl.summ_time_of_play_list
        assert str(duration) == '3:41:01'


    def test_show_best_video(self):
        """Проверка на вывод корректных данных"""
        pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
        pl.summ_time_of_play_list
        assert str(pl.show_best_video()) == 'https://youtu.be/9Bv2zltQKQA'

from utils.utils import *


# Объявление id каналов
channel_id_vdud = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
channel_id_edition = 'UC1eFXmJNkjITxPFWTy6RsWg'

# Создание экземпляра класса
channel = Channel()
# Добавление объекта API, изменяем
channel.add_object_youtube()

# Читаем и выводим инфо
channel.read_info(channel_id_vdud)
channel.print_info()

# Читаем и выводим инфо
channel.read_info(channel_id_edition)
channel.print_info()

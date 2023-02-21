from utils.utils import *


# Объявление id каналов
channel_id_vdud = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
channel_id_edition = 'UC1eFXmJNkjITxPFWTy6RsWg'

# Создание экземпляра класса
channel = Channel(channel_id_edition)

# Вывод содержимого переменных экземпляра
print(channel.channel_id)
print(channel.channel_name)
print(channel.channel_description)
print(channel.channel_link)
print(channel.number_of_subscriber)
print(channel.number_of_video)
print(channel.number_of_views)

# Объект для работы с API
print(channel.get_object_youtube())

# Создает фаил json
channel.to_json()

import configparser
import requests

config = configparser.ConfigParser()
config.read("config_bot.cfg")


class ExtractingUserData:
    def __init__(self):
        self.dict_photo_and_like = None
        self.user_id = None
        self.country = None
        self.sex = None
        self.city = None
        self.age_to = None
        self.age_from = None
        self.count = None
        self.paramitres = None
        self.token = config["TOKEN"]["vk_user_token"]

    def user_search(self, count, age_from, age_to, sex, city, country):
        """
        Метод поиска пользователей сайта VK по заданным параметрам, получает на вход параметры:

        count - количество найденых записей (не более 999)
        age_from - от какого возраста искать
        age_to - до какого возраста искать
        sex - пол (2 мужчина, 1 женщина)
        city - идентификаттор города (берется у пользователя который ведет диалог с ботом)
        country - идентификатор страны (берется у пользователя который ведет диалог с ботом)

        Поиск ведется ТОЛЬКО по страницам пользователей у которых установлен смейный статус "В активном поиске"
        :return:
        """
        self.count = count
        self.age_from = age_from
        self.age_to = age_to
        self.sex = sex
        self.city = city
        self.country = country

        self.paramitres = {'access_token': self.token, 'count': self.count, 'has_photo': 1, 'age_from': self.age_from,
                           'age_to': self.age_to, 'fields': 'photo_200_orig, relation: 6', 'sex': self.sex,
                           'city': self.city, 'country': self.country, 'v': 5.131}
        request_generation = requests.get(url=f'https://api.vk.com/method/users.search', params=self.paramitres)
        return request_generation.json()['response']['items']

    def photo_extraction(self, user_id):
        """
        Метод получения 3 фотографий пофиля которые имеют наибольшие LIKE, получает на вход параметры:

        user_id - id пользователя

        :return:
        """
        self.user_id = user_id
        self.dict_photo_and_like = {}
        self.paramitres = {'access_token': self.token, 'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1,
                           'photo_sizes': 0, 'v': 5.131}
        request_generation = requests.get(url=f'https://api.vk.com/method/photos.get', params=self.paramitres)

        for reqer in request_generation.json()['response']['items']:
            self.dict_photo_and_like[(reqer['sizes'][3]['url'])] = reqer['likes']['count']

        return sorted(self.dict_photo_and_like, key=self.dict_photo_and_like.get)[-3:]

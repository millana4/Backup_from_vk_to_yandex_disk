# Курсовой проект «Резервное копирование»

## мой id – 659301486
## id приложения 51437381
## access_token=vk1.a.1OxPDiFIwN6hMRlNx2vCAk9FHZKv1Hur_UJ0q9CojBChvpmrh6xShI-bt6K8HHUPedMqeDIknSlRFr30ASqzFYfiy9ulvElVTmWDGJBowpw5G5WNyuGpkzEeOcIVTQvBcLcafr5ARZSrBEp0VwAmiK371aO83_8slwBrSaoL-EcDW3I9DleEdEMSuMnkKkOe
## аутентификатор целиком https://oauth.vk.com/blank.html#access_token=vk1.a.1OxPDiFIwN6hMRlNx2vCAk9FHZKv1Hur_UJ0q9CojBChvpmrh6xShI-bt6K8HHUPedMqeDIknSlRFr30ASqzFYfiy9ulvElVTmWDGJBowpw5G5WNyuGpkzEeOcIVTQvBcLcafr5ARZSrBEp0VwAmiK371aO83_8slwBrSaoL-EcDW3I9DleEdEMSuMnkKkOe&expires_in=0&user_id=659301486


# Получение фотографий из профиля
import requests
import sys
import json
from pprint import pprint
import urllib.request

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_profile_pictures(self, id):
        """The function gets a dictionary with a profile picture in different types"""
        get_profile_pictures_url = self.url + 'photos.get'
        get_profile_pictures_params = {
            'owner_id': id,
            'album_id': 'profile',
            'photo_ids': [],
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(get_profile_pictures_url, params={**self.params, **get_profile_pictures_params}).json()
        with open('profile.json', 'w') as file:
            json.dump(res, file, indent = 4)
        return (res)

    def get_wall_pictures(self, id, count = 7):
        """The function gets a dictionary with wall pictures in different types"""
        get_wall_pictures_url = self.url + 'photos.get'
        get_wall_pictures_params = {
            'owner_id': id,
            'album_id': 'wall',
            'photo_ids': [],
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1,
            'count': count
        }
        res = requests.get(get_wall_pictures_url, params={**self.params, **get_wall_pictures_params}).json()
        with open('wall_pictures.json', 'w') as file:
            json.dump(res, file, indent=4)
        return (res)


# Сохранение фотографий на Яндекс.Диск
class Ya_Uploader:
    url = 'https://cloud-api.yandex.net'
    def __init__(self, my_ya_token):
        self.token = my_ya_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, need_id):
        """The function creates folder in Yansex.Disk. The folder gets name with ID"""
        create_folder_url = self.url + '/v1/disk/resources'
        headers = self.get_headers()
        folder_name = 'pictures_vk_id_' + need_id
        params = {'path': folder_name}
        requests.put(f'{create_folder_url}?path={folder_name}', headers=headers)
        return folder_name


## Сохрание на диск фото профиля
    def get_profile_picture(self, profile_dict):
        """The function creates a jpg-file in PyCharm project to prepare loading a profile picture to Yandex.Disk"""
        profile_pictures = profile_dict['response']['items'][0]['sizes']
        height = 0
        url = 0
        for picture in profile_pictures:
            if picture['height'] > height:
                height = picture['height']
                url = picture['url']
        picture_name = str(profile_dict['response']['items'][0]['likes']['count']) + '_profile.jpg'
        img = urllib.request.urlopen(url).read()
        out = open(picture_name, "wb")
        out.write(img)
        out.close
        return picture_name

    def get_upload_profile_picture_link(self, profile_picture, folder_name):
        """The function creates a link tp upload jpg-file"""
        upload_profile_picture_url = self.url +'/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': folder_name + "/" + profile_picture, 'overwrite': 'true'}
        response = requests.get(upload_profile_picture_url, headers=headers, params=params)
        return (response.json())

    def upload_profile_picture(self, profile_picture, folder_name):
        """The function uploads a profile picture to Yandex.Disk"""
        href = self.get_upload_profile_picture_link(profile_picture, folder_name).get('href', '')
        response = requests.put(href, data=open(profile_picture, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Фото профиля загружено на Яндекс.Диск')


## Сохранение на диск фото со стены
    def get_wall_pictures(self, wall_dict):
        """The function creates a jpg-files in PyCharm project to prepare loading wall pictures to Yandex.Disk"""
        wall_pictures = wall_dict['response']['items']
        wall_pictures_list = []
        for picture in wall_pictures:
            height = 0
            url = 0
            sizes = picture['sizes']
            for size in sizes:
                if size['height'] > height:
                    height = size['height']
                    url = size['url']
            date = picture['date']
            picture_name = str(picture['likes']['count']) + '.jpg'
            for image_name in wall_pictures_list:
                if image_name[0] == str(picture['likes']['count']):
                    picture_name = str(picture['likes']['count']) + '_date_' + str(date) + '.jpg'
                else:
                    picture_name = str(picture['likes']['count']) + '.jpg'
            img = urllib.request.urlopen(url).read()
            out = open(picture_name, "wb")
            out.write(img)
            out.close
            wall_pictures_list.append(picture_name)
        return (wall_pictures_list)

    def get_upload_wall_pictures_link(self, wall_picture, folder_name):
        """The function creates a link tp upload jpg-file"""
        upload_wall_picture_url = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': folder_name + "/" + wall_picture, 'overwrite': 'true'}
        response = requests.get(upload_wall_picture_url, headers=headers, params=params)
        return (response.json())

    def upload_wall_pictures(self, wall_pictures_list, folder_name):
        """The function uploads a profile picture to Yandex.Disk"""
        for wall_picture in wall_pictures_list:
          href = self.get_upload_wall_pictures_link(wall_picture, folder_name).get('href', '')
          response = requests.put(href, data=open(wall_picture, 'rb'))
          response.raise_for_status()
          if response.status_code == 201:
              print(f'Фото {wall_picture} загружено на Яндекс.Диск')

 #   def remove_temporary_files(self, profile_picture):



# удалить файл из каталога, сделать json, сделать файл зависимостей, токен Яндекса вводить

# Основная программа

if __name__ == '__main__':

    # Скачиваем снимки профиля и со стены ВКонтакте
    my_vk_token = 'vk1.a.1OxPDiFIwN6hMRlNx2vCAk9FHZKv1Hur_UJ0q9CojBChvpmrh6xShI-bt6K8HHUPedMqeDIknSlRFr30ASqzFYfiy9ulvElVTmWDGJBowpw5G5WNyuGpkzEeOcIVTQvBcLcafr5ARZSrBEp0VwAmiK371aO83_8slwBrSaoL-EcDW3I9DleEdEMSuMnkKkOe'
    last_version = '5.131'
    backup_save = VkUser(my_vk_token, last_version)
    # need_id = input('Введите ID пользователя, чьи фото нужно загрузить: ')
    need_id = '659301486'                ################ это потом убрать
    profile_dict = backup_save.get_profile_pictures(need_id)
    wall_dict = backup_save.get_wall_pictures(need_id)

    # Загружаем фото профиля на Яндекс.Диск
    my_ya_token = 'y0_AgAAAABa9ArWAADLWwAAAADP5shy7Baw-QirS1uXiBRhb1Z7jKbN-vc'
    uploader = Ya_Uploader(my_ya_token)
    uploader.create_folder(need_id)
    folder_name = uploader.create_folder(need_id)
    profile_picture = uploader.get_profile_picture(profile_dict)
    uploader.upload_profile_picture(profile_picture, folder_name)

    # Загружаем фото со стены на Яндекс.Диск
    wall_pictures_list = uploader.get_wall_pictures(wall_dict)
    uploader.upload_wall_pictures(wall_pictures_list, folder_name)





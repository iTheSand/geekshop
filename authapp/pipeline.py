from collections import OrderedDict
from datetime import date
from urllib.parse import urlunparse, urlencode

import requests
import urllib.request
from django.utils.datetime_safe import datetime
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max&access_token={response['access_token']}&v=5.92"

    # api_url = urlunparse(('https',
    #                       'api.vk.com',
    #                       '/method/users.get',
    #                       None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')), access_token=response['access_token'], v='5.92')),
    #                       None
    #                       ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    print(data)

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['photo_max']:
        # url = data['photo_max']
        # img = urllib.request.urlopen(url).read()
        photo = requests.get(data['photo_max'])

        if photo.status_code == 200:
            photo_name = f"/users_avatars/{user.username}.jpg"
            with open(f"media/{photo_name}", "wb") as avatar:
                avatar.write(photo.content)
                user.avatar = photo_name

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = int((date.today() - bdate).days / 365)
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.shopuserprofile.user.age = age
    user.save()

import vk_api
import urllib
import os
import datetime
import config

from .logger import log

class ImageDumper:
    def __init__(self):
        vk_session = vk_api.VkApi(token=config.TOKEN)
        self._vk = vk_session.get_api()
        log('Sucessfully authentificated')
    
    def get_images(self):
        log('Dumping friend list...')
        friends = self._get_frineds()
        log('You have {} friends'.format(len(friends)))

        log('Dumping photo\'s urls...')
        photos = []
        f_counter = 0
        for friend in friends:
            photo = self._dump_friend_images(friend)
            photos.append(photo)
            f_counter += 1
            log('({}/{}) - collected {} photos of {}'.format(f_counter, len(friends), len(photo['photos']), friend['name']))
        return photos

    def download_images(self, photos):
        log('Creating folders for photos...')
        root = self._create_image_folder(photos)
        log('Downloading images...')
        person = 0
        for photo in photos:
            person += 1
            name = 0
            log('({}/{}) - {}'.format(person, len(photos), photo['person']['name']))
            for image in photo['photos']:
                name += 1
                path = '{}/{}/{}.jpg'.format(root, photo['person']['name'], name)
                try:
                    urllib.request.urlretrieve(image, path)
                    log('\t({}/{}) photos downloaded'.format(name, len(photo['photos'])))
                except:
                    log('\t({}/{}) cannot download from url: {}'.format(name, len(photo['photos']), image))

    def _create_image_folder(self, photos):
        root = 'imagedump-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        if not os.path.exists(root):
            os.makedirs(root)
        for photo in photos:
            person_path = '{}/{}'.format(root, photo['person']['name'])
            if not os.path.exists(person_path):
                os.makedirs(person_path)
        return root

    def _get_frineds(self):
        res = self._vk.friends.get(order='hints', fields='nickname')
        friends = []
        for friend in res['items']:
            if friend['is_closed'] == True and friend['can_access_closed'] == False:
               continue
            friends.append({
                'id': friend['id'],
                'name': '{} {}'.format(friend['first_name'], friend['last_name'])
            })
        return friends

    def _dump_friend_images(self, friend):
        photos = {
            'person': friend,
            'photos': []
        }    

        res = self._vk.photos.getAll(owner_id=friend['id'], count=200, need_hidden=1)
        for photo in res['items']:
            photo = self._select_largest(photo['sizes'])
            photos['photos'].append(photo)

        count = res['count'] - 200
        i = 0
        for _ in range(1, count, 200):
            i += 1
            res = self._vk.photos.getAll(owner_id=friend['id'], count=200, offset=i*200, need_hidden=1)
            for photo in res['items']:
                photo = self._select_largest(photo['sizes'])
                photos['photos'].append(photo)  

        return photos
    
    def _select_largest(self, sizes):
        max_size = 0
        photo = ''
        for size in sizes:
            w = size['width']
            h = size['height']
            if w * h >= max_size:
                max_size = w * h
                photo = size['url']
        return photo
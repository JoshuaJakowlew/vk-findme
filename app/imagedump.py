import vk_api
import urllib
import os
import datetime
import config
import uuid

from .logger import log
from .photos_dumper import PhotosDumper
from .wall_dumper import WallDumper

_API_VERSION = '5.101' # Used VK API version

_MAX_FRIENDS = 5000    # Maximum number of friends/request
_MAX_PHOTOS  = 200     # Maximum number of photos/request

class ImageDumper:
    """Downloads all photos from users's friend list"""

    def __init__(self, verbose=True):
        """Authorizes user

        Args:
            verbose: If verbose=True then method writes logs
                If verbose=False then method keeps silence
        """

        vk_session = vk_api.VkApi(token=config.TOKEN, api_version=_API_VERSION)
        self._vk = vk_session.get_api()
        if verbose:
            log('Sucessfully authentificated')

    def dump_images(self, id=-1, verbose=True):
        """Downloads all photos from users's friend list

        Downloads all photos from pages that satisfy followong cases:
        - Page is user's friend
        - Page is active (field "deactivated" doesn't exist,
          see https://vk.com/dev/objects/user)
        - User has access to the page
          (is_closed == True and can_access_closed == False,
          see https://vk.com/dev/objects/user)
        
        Creates root folder with timestamp
        Then creates folder for each friend in a list inside root folder
        example:
        - imagedump-2019-08-18-00-49-56
        -- Павел Дуров-8a778108-b139-4317-befa-5734705ff197-145
        -- Lindsey Stirling-63ea671e-df77-44c9-8a65-cf979d818920-4

        Recieves photos of each friend and the downloads them
        If somethings went wrong and photo wasn't downloaded
        then this photo is skipped

        Args:
            id: User id.
                If id == -1 then id equals current (authorized) user's id
            verbose: If verbose=True then method writes logs
                If verbose=False then method keeps silence
        Returns:
            Tuple containing root path and number of downloaded photos
        """
        # Get all friends
        if verbose:
            log('Recieving friends...')
        friends = self._get_friends(id)
        
        # Create folders for photos
        if verbose:
            log('Creating folders...')
        root_folder, friend_folders = self._create_photos_folder(friends)

        friends = list(zip(friends, friend_folders))

        friend_n = 0
        for friend in friends:
            # Get photos's urls
            friend_n += 1
            if verbose:
                log(f"({friend_n}/{len(friends)}) Searching for {friend[0]['name']}'s photos")
            photos = self._get_photos(friend[0])
            
            # download photos
            if verbose:
                log(f'\t({len(photos)}) Downloading photos...')
            downloaded = self._download_photos(friend[1], photos)
            if verbose:
                log(f'\t({downloaded}) photos has been downloaded')

        return (root_folder, downloaded)

    # Photo methods

    def _create_photos_folder(self, friends):
        """Creates separate folders for each friend in a list

        Creates root folder with timestamp
        Then creates folder for each friend in a list inside root folder
        example:
        - imagedump-2019-08-18-00-49-56
        -- Павел Дуров
        -- Lindsey Stirling

        Args:
            friends: Array of dicts containing friend's id and full name
                (see _get_friends)
                example: 
                [
                    { 'id': 1, 'name': 'Павел Дуров' },
                    { 'id': 210700286, 'name': 'Lindsey Stirling' }
                ]
        Returns:
            Tuple containing root folder and list of nested folders
        """
        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        root = f'imagedump-{date}'

        if not os.path.exists(root):
            os.makedirs(root)

        friend_folders = []
        for friend in friends:
            friend_path = f"{root}/{friend['name']}-{uuid.uuid4()}"
            if not os.path.exists(friend_path):
                os.makedirs(friend_path)
                friend_folders.append(friend_path)

        return (root, friend_folders)

    def _download_photos(self, path, urls):
        """Download photos from urls to specified folder

        Args:
            path: Path to folder where all the photos wll be downloaded to
            urls: Array of photo urls
                (see _get_photos)
        Returns:
            Number of downloaded photos
        """
        counter = 0 # photo index number
        for url in urls:
            counter += 1
            file_path = f'{path}/{counter}.jpg'
            try:
                urllib.request.urlretrieve(url, file_path)
            except:
                counter -= 1
                continue
        return counter

    def _get_photos(self, friend):
        """Recieves friend's photos

         Recieves and parses friends photos
         Selects largest photo possible
         
         Args:
            friend: Dict containing friend's id and full name
                (see _get_friends)
                example: { 'id': 210700286, 'name': 'Lindsey Stirling' }
        Returns:
            Array of friend's photos url's
        """
        photos_dumper = PhotosDumper({ 'vk': self._vk })
        wall_dumper = WallDumper({ 'vk': self._vk })

        photos = photos_dumper.get_photos(friend['id'])
        photos.extend(wall_dumper.get_photos(friend['id']))
        return list(set(photos))

    # Friend methods

    def _get_friends(self, id=-1):
        """Recieves user's friends

        Recieves and parses user's friends.
        Uses current (authorized) user's id if not specified.
        Drops accounts with closed access.
        (is_closed == True and can_access_closed == False,
        see https://vk.com/dev/objects/user)

        Args:
            id: User id.
                If id == -1 then id equals current (authorized) user's id
        Returns: Array of dicts containing friend's id and full name
            example:
            [
                { 'id': 1, 'name': 'Павел Дуров' },
                { 'id': 210700286, 'name': 'Lindsey Stirling' }
            ]

        """     
        json_friends = self._recieve_friends_from_vk(id)
        return self._parse_friends_from_vk(json_friends)
    
    def _recieve_friends_from_vk(self, id):
        """Recieves friend list from VK

        Args:
            id: User id.
                If id == -1 then id equals current (authorized) user's id
        Returns:
            Array of VK user objects
            (see https://vk.com/dev/objects/user)
        """

        res = None
        if id == -1: # if no id specified
            res = self._vk.friends.get(order='hints', fields='nickname')
        else:
            res = self._vk.friends.get(user_id=id, order='hints', fields='nickname')
        count = res['count']
        json_friends = res['items']

        for i in range(_MAX_FRIENDS, count, _MAX_FRIENDS):
            res = None
            if id == -1: # if no id specified
                res = self._vk.friends.get(order='hints', offset=i, fields='nickname')
            else:
                res = self._vk.friends.get(user_id=id, offset=i, order='hints', fields='nickname')
            json_friends.extend(res['items'])

        return json_friends

    def _parse_friends_from_vk(self, json_friends):
        """Parses friend objects from VK

        Takes array of VK user objects and
        parses friend's id and first/last name.
        Drops accounts with closed access

        Args:
            json_friends: Array of VK friend objects
                (see https://vk.com/dev/friends.get)
        Returns:
            Array of dicts containing friend's id and full name
            example:
            [
                { 'id': 1, 'name': 'Павел Дуров' },
                { 'id': 210700286, 'name': 'Lindsey Stirling' }
            ]
        """
        friends = []

        for friend in json_friends:
            if 'deactivated' in friend:
                continue
            if friend['is_closed']         == True and \
               friend['can_access_closed'] == False:
               continue

            friends.append({
                'id': friend['id'],
                'name': '{} {}'.format(friend['first_name'], friend['last_name'])
            })
        return friends

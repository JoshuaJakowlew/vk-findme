from .base_dumper import BaseDumper

class WallDumper(BaseDumper):
    """Downloads all photos from wall"""

    _MAX_PHOTOS  = 100     # Maximum number of photos/request  

    def _receive_photos_from_vk(self, user_id):
        """Recieves friend's wallpost photo objects from VK

        Args:
            user_id: Target page id
        Returns:
            Array of VK photo objects
            (see https://vk.com/dev/objects/photo)
        """
        vk = self._ctx['vk']
        res = vk.wall.get(owner_id=user_id, count=self._MAX_PHOTOS)
        count = res['count']
        wall_posts = res['items']

        for i in range(self._MAX_PHOTOS, count, self._MAX_PHOTOS):
            res = vk.wall.get(owner_id=user_id, offset=i, count=self._MAX_PHOTOS)
            wall_posts.extend(res['items'])

        return wall_posts

    def _parse_photos(self, wall_posts):
        """Parses wallposts from VK

        Takes array of VK wallpost objects and parses url of the largest photo

        Args:
            wall_posts: Array of VK wallpost objects
                (see https://vk.com/dev/objects/photo)
        Returns:
            Array of friend's photos url's
        """

        json_photos = []
        wall_posts = list(filter(lambda post: 'attachments' in post, wall_posts))
        for post in wall_posts:           
            photo_attachments = list(filter(lambda a: a['type'] == 'photo', post['attachments']))
            photo_attachments = list(map(lambda a: a['photo'], photo_attachments))
            json_photos.extend(photo_attachments)

        return super(WallDumper, self)._parse_photos(json_photos)
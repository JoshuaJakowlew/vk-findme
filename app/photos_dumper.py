from .base_dumper import BaseDumper

class PhotosDumper(BaseDumper):
    """Downloads all photos from user's photos"""

    _MAX_PHOTOS  = 200     # Maximum number of photos/request  

    def _receive_photos_from_vk(self, user_id):
        """Recieves friend's photo objects from VK

        Args:
            user_id: Target page id
        Returns:
            Array of VK photo objects
            (see https://vk.com/dev/objects/photo)
        """
        vk = self._ctx['vk']
        res = vk.photos.getAll(owner_id=user_id, count=self._MAX_PHOTOS, need_hidden=1)
        count = res['count']
        json_photos = res['items']

        for i in range(self._MAX_PHOTOS, count, self._MAX_PHOTOS):
            res = vk.photos.getAll(owner_id=user_id, offset=i, count=self._MAX_PHOTOS, need_hidden=1)
            json_photos.extend(res['items'])

        return json_photos
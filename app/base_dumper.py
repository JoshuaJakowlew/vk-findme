class BaseDumper:
    """Interface for photo dumpers"""

    def __init__(self, ctx):
        self._ctx = ctx
    
    def get_photos(self, user_id):
        """Recieves friend's photos

         Recieves and parses friends photos
         Selects largest photo possible
         
         Args:
            user_id: Target page id
        Returns:
            Array of friend's photos url's
        """

        json_photos = self._receive_photos_from_vk(user_id)
        return self._parse_photos(json_photos)

    def _receive_photos_from_vk(self, id):
        """Interface"""
        raise NotImplementedError
    
    def _parse_photos(self, json_photos):
        """Parses photo objects from VK

        Takes array of VK photo objects and parses url of the largest photo

        Args:
                example: { 'id': 210700286, 'name': 'Lindsey Stirling' }
            json_photos: Array of VK photo objects
                (see https://vk.com/dev/objects/photo)
        Returns:
            Array of friend's photos url's
        """

        photos = []

        for photo in json_photos:
            url = self._select_largest_photo(photo['sizes'])
            photos.append(url)

        return photos

    def _select_largest_photo(self, sizes):
        """Selects photo with largest area
        
        Takes array of different photo sizes
        and selects photo with largestarea.
        Note, that photos uploaded before 2012 has
        "width" and "height" attributes equal to 0

        Args:
            sizes: "sizes" array from VK photo object
                (see https://vk.com/dev/objects/photo)
        Returns:
            biggest photo's url
        """

        max_size = 0
        photo = ''
        for size in sizes:
            w = size['width']
            h = size['height']
            if w * h >= max_size:
                max_size = w * h
                photo = size['url']
        return photo

import face_recognition as fr
import os

class FaceFinder:
    """This class allows you to find similar faces
    based on training set.
    """
    def __init__(self, train_path):
        """Looks at images in training set
        and calculates its face encodings

        Args:
            train_path: path to folder with training set
        """
        self._known_encodings = []

        for image_name in os.listdir(train_path):
            image_name = f'{train_path}/{image_name}'
            
            image_encoding = self.get_encoding(image_name)

            if image_encoding: 
                image_encoding = image_encoding[0] # select first face
                self._known_encodings.append(image_encoding)

    def find_face(self, image_path):
        """Finds face in test image and compares them
        to training set.
        This method is a shortcut for
        get_encoding + is_similar

        Args:
            image_path: Path to image in test set
        Returns:
            True if faces are similar, False if not
        """
        encoding = self.get_encoding(image_path)
        if not encoding:
            return False

        return self.is_similar(encoding)
    
    def get_encoding(self, image_path):
        """Given an image, return the 128-dimension
        face encoding for each face in the image.

        Args:
            image_path: Path to image in test set
        Returns:
            List of face encodings
            Empty list if there are no faces found
        """
        image = fr.load_image_file(image_path)

        face_locations = fr.face_locations(
            image, number_of_times_to_upsample=0, model="cnn")

        image_encoding = fr.face_encodings(
            image, known_face_locations=face_locations)

        return image_encoding

    def is_similar(self, test_image_encoding, treshold=0.6):
        """Determines whether faces in
        train_set and test image are similar

        Args:
            test_image_encoding: Encoding of test set image
                (see get_encoding())
            treshold: Faces with distance <= treshold are similar
                0.6 is default and fits for most cases
                try 0.5-0.55 for more strict results
        Returns:
            True if faces are similar, False if not
        """

        distances = self.calculate_distance(test_image_encoding)

        if not distances:
            return False

        for distance in distances:
            if distance <= treshold:
                return True
        return False

    def calculate_distance(self, test_image_encoding):
        """Calculates Euclidian distance between test set and given image

        Distance is an average of distances to every image in train set.
        If there are 3 images in test set and distances are
        [0.7, 0.55, 0.6]
        then resulting distance will be (0.7 + 0.55  +0.6) / 3 = 0.617

        Args:
            test_image_encoding: Encoding of test set image
                (see get_encoding())
        Returns:
            Empty list if there are no encodings in test_image_encoding
            List with average distances to every encoding in test_image_encoding
        """
        if not test_image_encoding:
            return []
        
        face_distances = []
        for encoding in test_image_encoding:
            distances = fr.face_distance(self._known_encodings, encoding)
            avg_distance = sum(distances)/len(distances)
            face_distances.append(avg_distance)
        
        return face_distances



        
            
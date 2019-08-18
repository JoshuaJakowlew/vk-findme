import face_recognition as fr
import os

class FaceFinder:
    def __init__(self, train_path):
        self._known_encodings = []

        for image_name in os.listdir(train_path):
            image_name = f'{train_path}/{image_name}'
            image = fr.load_image_file(image_name)
            face_locations = fr.face_locations(
                image, number_of_times_to_upsample=0, model="cnn")
            image_encoding = fr.face_encodings(
                image, known_face_locations=face_locations)
            if image_encoding: 
                image_encoding = image_encoding[0]
                self._known_encodings.append(image_encoding)

    def find_face(self, image_path):
        encoding = self.get_encoding(image_path)
        if not encoding:
            return False

        return self.is_similar(encoding)
    
    def get_encoding(self, image_path):
        image = fr.load_image_file(image_path)

        face_locations = fr.face_locations(
            image, number_of_times_to_upsample=0, model="cnn")

        image_encoding = fr.face_encodings(
            image, known_face_locations=face_locations)

        return image_encoding

    def is_similar(self, test_image_encoding, treshold=0.6):
        distances = self.calculate_distance(test_image_encoding)

        if not distances:
            return False

        for distance in distances:
            if distance <= treshold:
                return True
        return False


    def calculate_distance(self, test_image_encoding):
        if not test_image_encoding:
            return []
        
        face_distances = []
        for encoding in test_image_encoding:
            distances = fr.face_distance(self._known_encodings, encoding)
            avg_distance = sum(distances)/len(distances)
            face_distances.append(avg_distance)
        
        return face_distances



        
            
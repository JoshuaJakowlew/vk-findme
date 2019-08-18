from app.imagedump import ImageDumper
from app.face_finder import FaceFinder
import os
import shutil

# app version
VERSION = '1.0.0'

def main():
    # show name, version and license
    greeting()

    # create directory for training set
    # and ask user to put images in this folder
    prompt_for_training_set()

    # encode training set
    print('vk-findme > Training...')
    face_finder = FaceFinder('train_images')

    # dump images from VK
    print('vk-findme > Dumping images from VK...')
    image_dumper = ImageDumper()
    dumproot, _ = image_dumper.dump_images(id=448744461)

    # create directory for similar faces
    if not os.path.exists('similar_images'):
        os.mkdir('similar_images')

    print('vk-findme > Searching faces in test set...')
    call_for_test_set(face_finder, dumproot)

def greeting():
    print(f'VK-Findme v.{VERSION}')
    print('This software uses MIT license')

def prompt_for_training_set():
    if not os.path.exists('train_images'):
        os.mkdir('train_images')
        print('Put training images in "train_images" folder')
        os.system('pause')

def call_for_test_set(face_finder, dumproot):
    for friend_dir in os.listdir(dumproot):
        for image in os.listdir(f'{dumproot}/{friend_dir}'):
            image_path = f'{dumproot}/{friend_dir}/{image}'
            image_name = f'{friend_dir}-{image}'
            find_face(face_finder, image_path, image_name)

def find_face(face_finder, image_path, image_name):
    if face_finder.find_face(image_path):
        print(f'Face found! ({image_name})')
        shutil.copy2(image_path, f'similar_images/{image_name}')

if __name__ == '__main__':
    main()
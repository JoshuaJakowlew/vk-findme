from app.imagedump import ImageDumper
from app.face_finder import FaceFinder
import os
import shutil

# # dump images from VK
# image_dumper = ImageDumper()
# dumproot, _ = image_dumper.dump_images(id=448744461)

# encode training set
face_finder = FaceFinder('train_images')

dumproot = 'imagedump-2019-08-18-17-31-43'

# create directory for similar faces
if not os.path.exists('similar_images'):
    os.mkdir('similar_images')

for friend_dir in os.listdir(dumproot):
    for image in os.listdir(f'{dumproot}/{friend_dir}'):
        image_path = f'{dumproot}/{friend_dir}/{image}'
        image_name = f'{friend_dir}-{image}'
        res = face_finder.find_face(image_path)
        if res:
            print(f'Face found! ({image_name})')
            shutil.copy2(image_path, f'similar_images/{image_name}')

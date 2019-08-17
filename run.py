from app.imagedump import ImageDumper
import app.logger as logger

image_dumper = ImageDumper()
photos = image_dumper.get_images()
image_dumper.download_images(photos)

logger.flush()

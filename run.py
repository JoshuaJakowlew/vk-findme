from app.imagedump import ImageDumper
import app.logger as logger

image_dumper = ImageDumper()
image_dumper.dump_images()

logger.flush()

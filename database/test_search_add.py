from real_time_db1 import ImageProcessor
from db import ImageQuery

image_id = 5
image_path = 'home/image/6.jpg'
barcode = '123448'
product_name = 'A'
year='2024'
month='3'
day='13'
hour='8'
minute='15'
shift=3

processor=ImageProcessor()

processor.process_image(product_name,image_id,image_path, barcode,year,month,day,hour,minute,shift)
processor.record_search(barcode, product_name,image_id,year,month,day,shift)


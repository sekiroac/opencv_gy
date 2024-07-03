#只包括image_id,barcode,product_name。可以通过image_id查询，可以添加。

from peewee import *

db = SqliteDatabase('db.db')

class Smokebox(Model):
    class Meta:
        database = db
#表Image
class Image(Smokebox):
    image_id = AutoField(primary_key=True)
    barcode = CharField()
    product_name = CharField()


db.connect()
db.create_tables([Image])

#image_id查询
class ImageQuery:
    def query_images(self,image_id):
        try:
            s1 = Image.get(Image.image_id == image_id)
            print(s1.product_name)
        except Exception as e:
            print("数据不存在")

#添加
    def images_add(self,product_name,barcode,image_id):
        try:
            Image.create(barcode=barcode, product_name=product_name, image_id = image_id)
        except IntegrityError as e:
            print("这个ID已存在")

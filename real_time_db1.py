from peewee import *
#import datetime

real_time_db = SqliteDatabase('real_time_db.db')

class Smokebox(Model):
    class Meta:
        database = real_time_db
#表shift_set
class shift_set(Smokebox):
    shift = AutoField(primary_key=True)

    start_hour=CharField()
    start_minute=CharField()
    end_hour=CharField()
    end_minute=CharField()
#表Image
class Image(Smokebox):
    image_id = AutoField(primary_key=True)
    
    image_path = CharField()
    barcode = CharField()
    product_name = CharField()
    year = CharField()
    month = CharField()
    day = CharField()
    hour = CharField()
    minute = CharField()
    shift = IntegerField()


real_time_db.connect()

#删除表
#Image.drop_table()
#shift_set.drop_table()
#real_time_db.close()
real_time_db.create_tables([Image,shift_set])

#实时加入
class ImageProcessor:
    def process_image(self, product_name,image_id,image_path, barcode,year,month,day,hour,minute,shift):
        # 将图片信息保存到数据库中
        try:
            Image.create(image_path=image_path, barcode=barcode, product_name=product_name, image_id = image_id,year=year,month=month,day=day,hour=hour,minute=minute,shift=shift)
            #print("图片信息已保存到数据库中")
        except IntegrityError as e:
            print("图片信息已存在")
            print("image_id:",image_id)
            print("image_path:",image_path)
#历史查询
    def record_search(self, barcode, product_name,image_id,year,month,day,shift):
        count = 0

        try:
            conditions = []
            if barcode:
                conditions.append(Image.barcode == barcode)
            if product_name:
                conditions.append(Image.product_name == product_name)
            if image_id:
                conditions.append(Image.image_id == image_id)
            if year:
                conditions.append(Image.year == year)

            if month:
                conditions.append(Image.month == month)

            if day:
                conditions.append(Image.day == day)

            if shift:
                conditions.append(Image.shift == shift)
    
            query = Image.select().where(*conditions)

        except Exception as e:
            print("数据不存在")



        for image in query:
            count += 1
            print("Image_id:", image.image_id)
            print("Image_path:",image.image_path)
            print("Barcode:", image.barcode)
            print("Product_name:", image.product_name)
            print("Year:", image.year)
            print(count)



class ShiftSetting:

#添加班次设定
    def add_shift(self,start_hour,start_minute,end_hour,end_minute,shift):
        try:
            shift_set.create(shift=shift,start_hour=start_hour,start_minute=start_minute,end_hour=end_hour,end_minute=end_minute)

        except IntegrityError as e:
            print("保存失败！")


#更新班次
    def update_shift(self,old_shift,new_shift):
        #一次更换一个
        try:
            Image.update(shift=new_shift).where(shift_set.shift==old_shift).execute()
        except IntegrityError as e:
            print("更改失败！")
#更新班次设定
    def update_shift_setting(self,shift,new_start_hour,new_start_minute,new_end_hour,new_end_minute):
            #输入数组
        for a, new_start_hour in zip(shift, new_start_hour):
            try:
                shift_set.update(start_hour=new_start_hour).where(shift_set.shift == a).execute()
            except IntegrityError as e:
                print("更改失败！")
        
        for b, new_end_hour in zip(shift, new_end_hour):
            try:
                shift_set.update(end_hour=new_end_hour).where(shift_set.shift == b).execute()
            except IntegrityError as e:
                print("更改失败！")
    
        for c, new_start_minute in zip (shift, new_start_minute):
            try:
                shift_set.update(start_minute=new_start_minute).where(shift_set.shift == c).execute()
            except IntegrityError as e:
                print("更改失败！")

        for d, new_end_minute in zip(shift, new_end_minute):
            try:
                shift_set.update(end_minute=new_end_minute).where(shift_set.shift == d).execute()
            except IntegrityError as e:
                print("更改失败！")

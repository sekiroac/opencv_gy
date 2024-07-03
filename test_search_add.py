from real_time_db1 import ImageProcessor
import sqlite3
import random
conn = sqlite3.connect('real_time_db.db')
cur = conn.cursor()
""" 
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
pingpai = ["大丰收（软）01M","红金龙（硬红）01M","红金龙（软红之彩）01M","红金龙（软红之彩）02M","红金龙（软红之彩）03M"]
barcode = ['06103','02202','02180','02107','02162']
 """
processor=ImageProcessor()

cur.execute("DELETE FROM image")
conn.commit()

# processor.process_image(product_name,image_id,image_path, barcode,year,month,day,hour,minute,shift)




counter = 0
while counter < 500 :
    counter +=1 
    x1 = random.randint(0, 4)
    processor.process_image(pingpai[x1],counter,'image_path', barcode[x1],random.randint(1, 23)+2000,random.randint(1, 12),random.randint(1, 31),random.randint(1, 23),random.randint(1, 59),counter)


while counter < 40 :
    counter +=1 
    x2 = random.randint(0, 4)
    processor.process_image(pingpai[x2],counter,'image_path', barcode[x2],random.randint(1, 23)+2000,random.randint(1, 12),random.randint(1, 31),random.randint(1, 23),random.randint(1, 59),counter)



while counter < 60 :
    counter +=1 
    x3 = random.randint(0, 4)
    processor.process_image(pingpai[x3],counter,'image_path', barcode[x3],random.randint(1, 23)+2000,random.randint(1, 10),random.randint(1, 31),random.randint(1, 23),random.randint(1, 59),counter)



while counter < 80 :
    counter +=1 
    x4 = random.randint(0, 4)
    processor.process_image(pingpai[x4],counter,'image_path', barcode[x4],random.randint(1, 23)+2000,random.randint(1, 10),random.randint(1, 31),random.randint(1, 23),random.randint(1, 59),counter)


while counter < 100 :
    counter +=1 
    x5 = random.randint(0, 4)
    processor.process_image(pingpai[x5],counter,'image_path', barcode[x5],random.randint(1, 23)+2000,random.randint(1, 10),random.randint(1, 31),random.randint(1, 23),random.randint(1, 59),counter)







#processor.record_search(barcode, product_name,image_id,year,month,day,shift)

#processor.record_search('123448', 0,0,0,0,0,0)


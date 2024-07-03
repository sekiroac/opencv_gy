from real_time_db1 import ImageProcessor
from real_time_db1 import ShiftSetting
import sqlite3

processor=ImageProcessor()

shift_process=ShiftSetting()
conn = sqlite3.connect('./real_time_db.db')
cur = conn.cursor()
#cur.execute("SELECT start_hour FROM shift_set WHERE start_minute=='00'")

cur.execute("SELECT image_id FROM image") 
image_id_shift_set = cur.fetchall() #列表的id号码
lenxx = len(image_id_shift_set)
print(lenxx)

from real_time_db1 import ImageProcessor
from real_time_db1 import ShiftSetting

processor=ImageProcessor()

shift_process=ShiftSetting()

#start_hour='5'
#start_minute='15'
#end_hour='7'
#end_minute='45'
#shift=1

#shift_process.add_shift(start_hour,start_minute,end_hour,end_minute,shift)

#old_shift=2
#new_shift=5
#shift_process.update_shift(old_shift,new_shift)


new_start_hour=[6,9,12]
new_start_minute=[25,15,35]
new_end_hour=[8,11,14]
new_end_minute=[35,15,45]
shift = [1, 2, 3]
shift_process.update_shift_setting(shift,new_start_hour, new_start_minute, new_end_hour, new_end_minute)
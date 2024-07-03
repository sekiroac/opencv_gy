import cv2
import numpy as np

import mycvtool

template=cv2.imread("./newnum.jpg")
template_gray=cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)

mycvtool.myshow("template_gray",template_gray)


_,template_threshold=cv2.threshold(template_gray.copy(),127,255,cv2.THRESH_BINARY_INV)
mycvtool.myshow("tt",template_threshold)

temp=template_threshold.copy()

mycvtool.myshow("tp",temp)
contours,hierachy=cv2.findContours(template_threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

print(np.array(contours).shape)

#sortlist=[cv2.boundingRect(contour) for contour in contours]
sortlist=[]
for contour in contours:
    rec=cv2.boundingRect(contour)
    sortlist.append(rec)

#print(sortlist)
#sortedlist=sorted(sortlist,key=lambda c:c[0])

(conts,rects)=zip(*sorted(zip(contours,sortlist),key=lambda a:a[1][0]))
#每个数字的roi进字典
templates={}
for index,c in enumerate(conts):
    x,y,w,h=cv2.boundingRect(c)
    roi=temp[y:y+h,x:x+w]#调整ROI区域,四周预留3像素
    templates[index]=roi
 #存储0-9   
    temper=cv2.resize(roi,(50,80))
    cv2.imwrite("./templates/"+str(index)+".jpg",temper)


""" testTemp=cv2.resize(templates[2],(50,80))
testTemp5=cv2.resize(templates[5],(50,80))
cv2.imwrite("./templates/2.jpg",testTemp)
cv2.imwrite("./templates/5.jpg",testTemp5)  """


cv2.destroyAllWindows()


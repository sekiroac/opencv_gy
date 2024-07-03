import cv2
import numpy as np


def myshow(window_name,image):
    cv2.imshow(window_name,image)
    cv2.waitKey()

def perspect_Adjust(per_src,boxWaitingTrans,transformed_w,transformed_h):#(调整的源图片，要调整的box，调整后的宽，调整后的高)，返回调整后的四个结果
      Adbox=[]
      #定义四个点
      fourPoints=[[0,0],[transformed_w,0],[transformed_w,transformed_h],[0,transformed_h]]
      for stp in range(len(fourPoints)): #四个循环
             actualRound=fourPoints[stp:]+fourPoints[:stp]
             perspectivebox=np.float32(actualRound)
             pers=cv2.getPerspectiveTransform(boxWaitingTrans,perspectivebox)
             dst = cv2.warpPerspective(per_src,pers,(5+int(transformed_w),5+int(transformed_h)))
             Adbox.append(dst)
      return Adbox

def stack_image(imagelist):
      '''
        [[],[]]
        [[],[]]

      ''' 
      vertical_count=len(imagelist)+1
      horizon_count=len(imagelist[1])+1
      
      return
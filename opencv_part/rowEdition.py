import cv2 
import numpy as np

from . import mycvtool 
from . import Match



def Test(picPath):
        #读取模板
    templates=[]
    for index in range(10):
        path=r"C:\Users\sekiro\Desktop\Projectzhou\GUI\opencv_part\templates\{}".format(str(index))+".jpg"
        
        templates.append(cv2.imread(path,-1))
    print("tem:",len(templates))
        #读取
    #picT = cv2.imread(r'{}'.format(picPath))#('',0)读取为单通道灰度图
    
    picT = cv2.imread(picPath)#('',0)读取为单通道灰度图
        #滤波
    pictrb=cv2.GaussianBlur(picT,(5,5),0)
        
        #转为单通道灰度图
    picTr=cv2.cvtColor(pictrb,cv2.COLOR_BGR2GRAY)

        #二值化   
    retval,picTr=cv2.threshold(picTr,26,255,cv2.THRESH_BINARY_INV)#返回  阈值retval，处理后的图 picTr
    #picTr=cv2.adaptiveThreshold(picTr,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15,5)
    #cv2.imshow("223",picTr)
    
        #形态学处理，膨胀数字
    #kernel = np.ones((3,3),np.uint8) 
    #erosion_1 = cv2.erode(picTr,kernel,iterations = 1)
    #cv2.imshow("224",erosion_1)
    k=np.ones((9,9),np.uint8)
    pictrb1=cv2.dilate(picTr,k,iterations=1)

        #pictrb1=cv2.medianBlur(picTr,5)
    #cv2.imshow("22",pictrb1)
    #cv2.waitKey()
        
        #轮廓查找
    picTr_contours,hierarchy=cv2.findContours(pictrb1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#返回 轮廓contour,层级,contour是list，不是ndarray

        #绘制轮廓
    picT_drawcoutours=picT.copy()
    cv2.drawContours(picT_drawcoutours,picTr_contours,-1,(0,255,0),2)
    #mycvtool.myshow("dsds",picT_drawcoutours)    

    h,w,channel=picT.shape#先h，后w,.shape先行后列
        #绘制最小外接矩形
    class Pattern:               #定义一个图片类
        def __init__(self,contour,ratio,flag):
            self.contour=contour
            self.ratio=ratio
            self.isNumber= flag
            self.rect=cv2.minAreaRect(self.contour)
            self.rectbox=np.uint0(cv2.boxPoints(self.rect))
            self.x,self.y,self.w,self.h=cv2.boundingRect(self.contour)


    #\按长宽比筛选数字
    patterns=[]

    for i in range(len(picTr_contours)):
        flag=False
        rect=cv2.minAreaRect(picTr_contours[i])                     #最小外接矩形
        center,size,angle=rect  
        
        width,height=size
       
        print(size,width/height,height/width,width*height)
        if width*height<=1500 or width*height>=3000:
              continue
        else:
            if(height>width):           #统一长宽比
                        ratio=height/width   
            else:
                        ratio=width/height
                #print(height,width,ratio)
            if((ratio>=1.5)and(ratio<=1.85)):
                    
                        patterns.append(Pattern(picTr_contours[i],ratio,True))
            elif((ratio>=2.3)and(ratio<=2.7)):
                        
                        patterns.append(Pattern(picTr_contours[i],ratio,True))

    #中心距搜索算法
    ##for i in range(len(picTr_contours)):
        
          
    
    target=[]
    print(len(patterns))
    for i in range(len(patterns)-4):
                if all(patterns[i+j].isNumber==True for j in range(5)):
                    target=patterns[i:i+5]
                    
    print(len(target))
    if(len(target)!=5):
        print(len(target))
        print("对不起，未识别到有效品牌号码")
        return 
   
    #将数字区域框出
    #最小框
    rectangles=[]
    for i in range(len(target)):
        rectangles.append(target[i].rectbox)

    merged_rect=np.vstack(rectangles)


    box0=np.uint0(cv2.boxPoints(cv2.minAreaRect(merged_rect)))
    xt,yt,wt,ht=cv2.boundingRect(merged_rect)
    testb=picT.copy()
    cv2.rectangle(testb, (xt, yt), (xt+wt, yt+ht), (0, 255, 0), 2)
    #cv2.imshow("testb",testb)
    _,(wd,hg),_=cv2.minAreaRect(merged_rect)
    boxt=np.array(box0,dtype=np.int32)   #最小框角点
    box_waiting_pers=np.float32(box0)
    testcopy=picT.copy()
    cv2.polylines(testcopy, [boxt], isClosed=True, color=(255), thickness=2)
    mycvtool.myshow("testcopy",testcopy)
    #cv2.imshow("rectsd",merged_rect_pic) """


    #首先box_waiting_pers中的x最小的点为1号点，其他点为顺时针方向顺次234，于是只要判断1号点的四种情况（0,0），(x,0),(x,y),(0,y)
    if hg>wd:
        real_wd=hg
        real_hg=wd
    else:
        real_wd=wd
        real_hg=hg   
    #print(wd,hg)

    #透视摆正
    dsts=mycvtool.perspect_Adjust(picTr,box_waiting_pers,real_wd,real_hg)
    for dst in dsts:
        numbers=[]
        k2=np.ones((5,5),np.uint8)
        dstp=cv2.dilate(dst,k2)
        sec_contours,_=cv2.findContours(dstp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if(len(sec_contours)!=5):
                continue

        #把轮廓从左向右排序，依据：最小外接矩形的center的x坐标
        numberContour=[]
        for i in range(len(sec_contours)):  #5次循环
            numberRect=cv2.minAreaRect(sec_contours[i])
            numberContour.append((sec_contours[i],numberRect[0]))

        sorted_numberContour=sorted(numberContour,key=lambda x:x[1][0])#[((contour),(center_x,center_y))]

        #把排序好的轮廓放到numbers列表里
        for i in range(len(sorted_numberContour)):
            #print(sorted_numberContour[i][0],type(sorted_numberContour[i][0]))
            number=Pattern(sorted_numberContour[i][0],_,True)
            numbers.append(number)
        #匹配
        result=[]
        for number in numbers:
            #print(number.rectbox)
                roi_n=dstp[number.y:number.y+number.h,number.x:number.x+number.w]
                numberAd=cv2.resize(roi_n,(50,80))
                #mycvtool.myshow("region",numberAd)
                #simi,resultNumber,matchresult=Match.matchNumber(numberAd,templates)
                simi,resultNumber,matchresult=Match.MatchTemplates_SqD(numberAd,templates)
                #print(simi)
                #筛选翻转180度的数字
                if(simi>=25000000):
                    result.clear
                    break
                else:
                    result.append(resultNumber) 
    
        if len(result)==5:
            #cv2.imshow("dstp",dstp)   
            #print("识别为")
            res="".join(map(str,result))
            print("识别的数字是"+res) #对result里的每个元素进行str操作，并加到空字符串  
            return res 
            
        else:
             #print("未识别到有效字段")
             #print(len(result))
             continue
        
        #show
        
        cv2.waitKey() 


    cv2.destroyAllWindows()



if __name__=="_main_":
    Test()



#perspectivebox=np.float32([[0,hg],[0,0],[wd,0],[wd,hg]])
#pers=cv2.getPerspectiveTransform(box_waiting_pers,perspectivebox)
#dstp = cv2.warpPerspective(picTr,pers,(5+int(wd),5+int(hg)))
#cv2.imshow("dstp",dstp)

""" print(wm,hm)

#从这里开始写：取target的中间那个数的contour,把图像整体旋转到正，再处理：
print(target[2].ratio)
Ad_center,_,Ad_angle=cv2.minAreaRect(target[2].contour) 
print("angle:",Ad_angle)
if(Ad_angle<45):
       compensate_angle=90
else:
       compensate_angle=0
rotateMatrix=cv2.getRotationMatrix2D(Ad_center,Ad_angle+compensate_angle,1)
#rotatedPic=cv2.warpAffine(picTr.copy(),rotateMatrix,(w,h))  
rotatedPic=cv2.warpAffine(merged_rect_pic,rotateMatrix,(800,800)) 
cv2.imshow("rotated",rotatedPic)  
cv2.waitKey()     
#再次查找轮廓
ro_contours,_=cv2.findContours(pictrb1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    """
    



""" picT_copy=picT.copy()                            #rect是一个包含（x,y）矩形中心坐标、(w,h)长宽尺寸，angle旋转角度的元组
    rotateMatrix=cv2.getRotationMatrix2D(center,angle,1)        #获取旋转矩阵，angle正为逆时针
    rotationAdjustedPic=cv2.warpAffine(picT_copy,rotateMatrix,(w,h))
    box=np.int0(cv2.boxPoints(rect))                            #获取矩形四个点的整数参数
    uint_box=np.int0(box)
    x1,y1,w1,h1=cv2.boundingRect(uint_box)

    roi=rotationAdjustedPic[y1:y1+h1,x1:x1+w1]
    cv2.imshow("rt",rotationAdjustedPic)
    cv2.imshow("p"+str(i),roi)
    cv2.waitKey() """


'''
    #绘制最小外接矩形
    rect0=cv2.minAreaRect(picTr_contours[2])
    box0=cv2.boxPoints(rect0)
    uint_box0=np.int0(box0)  
    x0,y0=uint_box0[0]
    x1,y1=uint_box0[1]
    x2,y2=uint_box0[2]
    x3,y3=uint_box0[3]
    print(np.array(picTr_contours).shape,type(np.array(picTr_contours).shape))
    print(uint_box0)

    picT_c=picT.copy()
    former =np.float32([[x0,y0],[x1,y1],[x2,y2],[x3,y3]])
    cv2.rectangle(picT_c,(x0,y0),(x2,y2),(0,0,255),2)
    now=np.float32([[50,80],[0,80],[0,0],[50,0]])
   

    a1=0
    a2=0
    b1=0
    b2=0
    if(y2>y0):
        a1=y0
        a2=y2
    else:
        a1=y2
        a2=y0
   
    if(x2>x0):
        b1=x0
        b2=x2
    else:
        b1=x2
        b2=x0
    roi=picTr[a1:a2,b1:b2]#_,_前面要小于后面,改进,还有长宽比
    ratio=(a2-a1)/(b2-b1)#changkuanbi
    print(ratio)

    m5=cv2.getPerspectiveTransform(former,now)
    sm5=cv2.warpPerspective(picTr,m5,(50,80))
    
    cv2.imwrite("./testnumber5.jpg",sm5)
  

    cv2.imshow("dr",picT_c)
    cv2.imshow("tr",sm5)
    cv2.imshow("tt",roi)
    cv2.imwrite("./test5.jpg",cv2.rotate(roi,1))
    cv2.waitKey()
   
    #float 需要转化为int
    
   
    cv2.drawContours(picT_copy,[uint_box0],0,(0,0,255),2)

    cv2.imshow('picTr_contour',picT_copy)
    cv2.waitKey()
    #cv2.imshow('picTr',picTr)

    #print(picT.shape)
    '''
    #cv2.waitKey()
   



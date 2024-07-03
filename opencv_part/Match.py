import cv2
import numpy as np
from . import mycvtool


#匹配
def matchNumber(testpattern,templates):  #传入一个testpattern，返回一个最高分匹配:遍历十个模版，把每个模板的similarity存到Matchresult,返回matchresult的最大值与最大值索引
    same=0
    differ=0
    similarity=0.00
    Matchresult=[]
    #二值化
    for idx in range(len(templates)):
        _,testpattern_th=cv2.threshold(testpattern,50,255,cv2.THRESH_BINARY)
        _,template_th=cv2.threshold(templates[idx],50,255,cv2.THRESH_BINARY)
        
        for row in range(0,testpattern_th.shape[0]):
            for col in range(0,template_th.shape[1]):
                if(testpattern_th[row][col]==template_th[row][col]):
                    same=same+1
                else:
                    differ=differ+1
        similarity=same/(same+differ)
        Matchresult.append(similarity)
    max_val=max(Matchresult)
    max_idx=Matchresult.index(max_val)
    return max_val,max_idx,Matchresult


def MatchTemplates_SqD(testpic,templates): #平方差匹配，遍历十个模板，
    matchresult=[]
    for idx in range(len(templates)):
        minus=0
        SqD=0
        

        _,testpattern_th=cv2.threshold(testpic,50,255,cv2.THRESH_BINARY)
        _,template_th=cv2.threshold(templates[idx],50,255,cv2.THRESH_BINARY)
        
        for row in range(0,template_th.shape[0]):
            for col in range(0,templates[idx].shape[1]):
                minus=abs(template_th[row][col]-testpattern_th[row][col])
                minusSquare=minus**2
                SqD=SqD+minusSquare
        matchresult.append(SqD)
    min_val=min(matchresult)
    min_idx=matchresult.index(min_val)
    return min_val,min_idx,matchresult
#####

""" result=[]
for i in range(len(templates)):
    
    result.append(matchNumber(number2,templates[i]))
print(result)
max_result=max(result)
max_idx=result.index(max_result)
min_result=min(result)
min_idx=(result.index(min_result))
print(max_idx)
print(max_result)
print(min_idx)
print(min_result)
 """

        









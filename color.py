import numpy as np
import cv2
import os 
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--grade", required=True,
                help="type the grade of the fruit")

args = vars(ap.parse_args())

directory = 'data_v2/val/' + args["grade"] + '/'

store_b=[]
store_g=[]
store_r=[]
store_path=[]

for filename in os.listdir(directory):
        img = cv2.imread(os.path.join(directory, filename))
        cp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(cp,150,255,0)
        # cv2.imshow('img',thresh) 
        cv2.waitKey(0)
        # im2,contours,hierarchy = cv2.findContours(thresh.astype(np.uint8), 1, 2)
        contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts = contours
        b_=[] 
        g_=[] 
        r_=[] 
        
        for cnt in cnts:
                if cv2.contourArea(cnt) >800: # filter small contours
                        x,y,w,h = cv2.boundingRect(cnt) # offsets - with this you get 'mask'
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                        #cv2.imshow('cutted contour',img[y:y+h,x:x+w])
                        b,g,r=np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)[0],np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)[1],np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)[2]
                        #print('Average color (BGR): ',b,g,r)
                        b_.append(b)
                        g_.append(g)
                        r_.append(r)

        #find the index of the max value in the list r
        max_r=r_.index(max(r_))

        # print corresponding values of index max_r in r,g,b lists
        print(r_[max_r],g_[max_r], b_[max_r])
        store_r.append(str(r_[max_r]))
        store_g.append(str(g_[max_r]))
        store_b.append(str(b_[max_r]))
        store_path.append(os.path.join(directory,filename))
        
        

print('RGB Values of', len(store_b), 'images have been calculated and stored in the .csv file')
dict = {'r_value': store_r, 'g_value': store_g, 'b_value': store_b, 'label': args['grade']}
df = pd.DataFrame(dict)
df.to_csv('data_v2/csv/val/color/color' + args['grade'] + '.csv', index=False)
# df.to_csv('data_v2/val_ind.csv', index=True)



import cv2
import numpy
import os 
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--grade", required=True,
                help="type the grade of the fruit")

args = vars(ap.parse_args())

def grab_contours(cnts):
    # OpenCV v2.4, v4-official
    if len(cnts) == 2:
        return cnts[0]
    # OpenCV v3
    elif len(cnts) == 3:
        return cnts[1]

directory = 'data_v2/val/' + args["grade"] + '/'

area_list=[]
perimeter_list=[]
cnt_list = 0
w_list = []
w_act=[]
h_list = []
h_act =[]

for filename in os.listdir(directory):

    image = cv2.imread(os.path.join(directory,filename))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 240, 250)
    # cv2.imshow("canny", edged)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)

    contour_image = edged.copy()
    area = 0
    perimeter = 0

    for c in cnts:
        area += cv2.contourArea(c) 
        perimeter += cv2.arcLength(cnts[0],True)
        _,_,w,h = cv2.boundingRect(c)

        w_list.append(w)
        h_list.append(h)
        
        cv2.drawContours(contour_image,[c], 0, (100,5,10), 3)
    
    h_act.append(max(h_list))
    w_act.append(max(w_list))
    cnt_list+= len(cnts)
    area_list.append(area)
    perimeter_list.append(perimeter/5)

# print(len(w_act), len(h_act))
#print(cnt_list//306)
   
print('Areas of', len(area_list), 'images have been calculated and stored in the .csv file')

dict = {'area': area_list, 'perimeter': perimeter_list, 'height': h_act, 'width': w_act, 'label': args['grade']}
df = pd.DataFrame(dict)
df.to_csv('data_v2/csv/val/areas/area' + args['grade'] + '.csv', index=False)

# cv2.putText(contour_image, str(area), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
# cv2.imshow("area", contour_image)
# cv2.waitKey(0)
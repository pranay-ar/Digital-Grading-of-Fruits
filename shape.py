import numpy as np
import cv2
import os 
import pandas as pd 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--grade", required=True,
                help="type the grade of the fruit")

args = vars(ap.parse_args())
 
# grade = str(9)

directory = 'data_v2/val/' + args["grade"] + '/'

index = []

for filename in os.listdir(directory):
    # Load the image
    img = cv2.imread(os.path.join(directory,filename))
    # Convert to greyscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert to binary image by thresholding
    _, threshold = cv2.threshold(img_gray, 245, 255, cv2.THRESH_BINARY_INV)
    # Find the contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    area=[]
    approx_=[]

    # For each contour approximate the curve and
    # detect the shapes.
    for cnt in contours:
        epsilon = 0.01*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(img, [approx], 0, (0), 3)
        # Position for writing text
        x,y = approx[0][0]

        area.append(cv2.contourArea(cnt)) 
        approx_.append(len(approx))
        
    # match highest area contour
    max_area = max(area)
    max_index = area.index(max_area)
    # print(approx_[max_index])

    # print(approx_[max_index])
    index.append(approx_[max_index])

    if approx_[max_index] == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 0,2)
    elif approx_[max_index] == 4:
        cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 0,2)
    elif approx_[max_index] == 5:
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 0,2)
    elif 6 < approx_[max_index] < 15:
        cv2.putText(img, "Ellipse", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 0,2)
    else:
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 0,2)

    # cv2.imshow("final", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

print('Indices of', len(index), 'images have been calculated and stored in the .csv file')
dict = {'index': index, 'label': args['grade']}
df = pd.DataFrame(dict)
df.to_csv('data_v2/csv/val/shape/index'+ args['grade'] + '.csv', index=False)
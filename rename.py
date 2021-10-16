# Pythono3 code to rename multiple 
# files in a directory or folder
  
# importing os module
import os
  
# Function to rename multiple files
def main():
  
    for count, filename in enumerate(os.listdir("data_v2/val/1/")):
        dst ="data_v2/val/1/" + "grade_1_" + str(count) + ".jpg"
        src ="data_v2/val/1/"+ filename
          
        # rename() function will
        # rename all the files
        os.rename(src, dst)
  
# Driver Code
if __name__ == '__main__':
      
    # Calling main() function
    main()
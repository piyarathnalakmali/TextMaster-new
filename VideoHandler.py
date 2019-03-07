import cv2
import numpy as np
import os
import math

from Image import Image

class VideoHandler:
    images = []
    videos = []
    object_array=[]
    similarFrames=[]
    def __init__(self):
        return None

    def addVideo(self,video):
        self.videos.append(video)

    def splitVideo(self,video):

        try:
            if not os.path.exists('data'):
                os.makedirs('data')
        except OSError:
            print ('Error: Creating directory of data')

        cap = cv2.VideoCapture(video.path)
        frameRate = cap.get(5) #frame rate
        x=1
        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number
            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate*8) == 0):
                filename = './data/frame' +  str(int(x)) + ".jpg";
                imagename='frame'+str(int(x)) + '.jpg'
                image=Image(filename,imagename)
                self.object_array.append(image)
                self.images.append(imagename)
                x+=1
                cv2.imwrite(filename, frame)

        cap.release()
        print ("Done!")
        print (self.images)
        print([x.name for x in self.object_array])

    def compareImages(self):
        for i in range (0,len(self.object_array)-2):
            original = cv2.imread(self.object_array[i].path)
            image_to_compare = cv2.imread(self.object_array[i+1].path)

            # 1) Check if 2 images are equals
            if original.shape == image_to_compare.shape:
                print("The images have same size and channels")
                difference = cv2.subtract(original, image_to_compare)
                b, g, r = cv2.split(difference)

                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print("The images are completely Equal")
                else:
                    print("The images are NOT equal")
                    # 2) Check for similarities between the 2 images

                    sift = cv2.xfeatures2d.SIFT_create()
                    kp_1, desc_1 = sift.detectAndCompute(original, None)
                    kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
                    index_params = dict(algorithm=0, trees=5)
                    search_params = dict()
                    flann = cv2.FlannBasedMatcher(index_params, search_params)

                    matches = flann.knnMatch(desc_1, desc_2, k=2)
                    good_points = []
                    ratio = 0.2
                    for m, n in matches:
                        if m.distance < ratio*n.distance:
                            good_points.append(m)
                    print (len(good_points))
                    if (len(good_points)>175):
                        self.similarFrames.append(self.object_array[i+1].path)
                        self.images.remove(self.object_array[i+1].name)
        for i in self.similarFrames:
            os.remove(i)
        print (self.images)

    def generateTextFile(self):
        try:
            from PIL import Image
        except ImportError:
            import Image
        import pytesseract
        f= open("Text.txt","a")
        for x in self.images:
            text = pytesseract.image_to_string(Image.open('./data/'+x))
            f.write(text+"\n"+"---------------PAGE BREAK----------------------------------"+"\n")
        f.close()
        textFile=open("Text.txt","r")
        return textFile.readlines()

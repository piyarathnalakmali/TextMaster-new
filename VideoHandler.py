import cv2
import numpy as np
import os
import math
import codecs
from Image import Image


class VideoHandler:
    images = []
    videos = []
    object_array=[]
    similarFrames=[]

    def __init__(self):
        return None

    def deleteVideo(self,video):
        self.videos.remove(video)
        os.remove(video.path)

    def addVideo(self,video):
        for exVideo in self.videos:
            if exVideo.user==video.user:
                self.deleteVideo(exVideo)
        self.videos.append(video)

    def getVideoByUserId(self,user_id):
        for video in self.videos:
            if video.getId()==user_id:
                return video

    def convertTime(self,millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = int(math.floor((millis / (1000 * 60 * 60)) % 24))
        return "%02d"%(minutes,)+":"+"%02d"%(seconds,)+".000"
    def splitVideo(self,video):

        try:
            if not os.path.exists('data/'+video.getId()):
                os.makedirs('data/'+video.getId())
        except OSError:
            print ('Error: Creating directory of data')

        cap = cv2.VideoCapture(video.path)
        frameRate = cap.get(5) #frame rate
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #get length of the video


        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number
            frameTime=cap.get(cv2.CAP_PROP_POS_MSEC)
            time = self.convertTime(frameTime)


            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate*8) == 0):
                filename = 'data/'+video.getId()+'/frame' + str(frameId) + ".jpg";
                imagename='frame'+str(frameId) + '.jpg'
                image=Image(filename, imagename,time);
                self.object_array.append(image)
                self.images.append(imagename)
                cv2.imwrite(filename, frame)

        cap.release()
        print ("Done!")
        print (self.images)
        # os.chdir('../')
        print([x.path for x in self.object_array])



    def compareImages(self):
        for i in range (0,len(self.object_array)-2):
            original = cv2.imread(self.object_array[i].path)
            print(self.object_array[i].path)
            image_to_compare = cv2.imread(self.object_array[i+1].path)
            print(self.object_array[i+1].path)
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
                        self.similarFrames.append(self.object_array[i+1])
                        # self.images.remove(self.object_array[i+1].name)
        for i in self.similarFrames:
            os.remove(i.path)
            self.object_array.remove(i)
        print (self.object_array)

    def generateTextFile(self,video):
        try:
            from PIL import Image
        except ImportError:
            import Image
        import pytesseract
        # f = codecs.open("text/"+video.getId()+".vtt","w",'utf-8')
        f = open("text/"+video.getId()+".vtt","w",encoding='utf-8')
        txtFile = open("text/"+video.getId()+".txt","w",encoding='utf-8')
        f.write("WEBVTT \n")
        temp=''
        tempText ='';
        finalText = '';
        for x in self.object_array:
            text = pytesseract.image_to_string(Image.open(x.path))
            if not (temp == ''):
                newTime = temp+" --> "+x.time
                text.rsplit()
                te = text.split("\n")
                text = ''
                print(te)
                for i in te:
                    if not i == '':
                        text+='- '+i+"\n"
                temp = x.time
                f.write("\n"+newTime+"\n"+finalText)
                txtFile.write("\n"+finalText+" ------------------------------------ ")
                finalText = text
            else:
                temp = x.time
                te = text.split("\n")
                text = ''
                print(te)
                for i in te:
                    if not i == '':
                        text += '- '+ i + "\n"
                temp = x.time
                finalText = text

            # f.write(text+"\n"+"---------------PAGE BREAK----------------------------------"+"\n")
        f.close()
        txtFile.close()
        txtFile = open("text/"+video.getId()+".txt","r",encoding='utf-8')
        s = txtFile.read()

        return s

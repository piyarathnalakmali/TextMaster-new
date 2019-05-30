class Image():
    def __init__(self,imagePath,imageName,imageTime):
        self.name=imageName
        self.path=imagePath
        self.time=imageTime
        return None

    def setLastTime(self,lastTime):
        self.lastTime = lastTime

class Video():
    def __init__(self, filename,path,user_id):
        self.name=filename
        self.path=path
        self.user=user_id
    def getName(self):
        return self.name

    def getId(self):
        return self.user

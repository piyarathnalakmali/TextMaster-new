import os
from flask import Flask , render_template , request
from Video import Video
from VideoHandler import VideoHandler

app=Flask(__name__)

videoHandler = VideoHandler()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload' , methods = ["POST"])
def upload():
    target=os.path.join(APP_ROOT, 'videos/')
    print (target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print (file)
        filename=file.filename
        destination = "/".join([target,filename])
        print(destination)
        file.save(destination)
        video = Video(filename,destination)
        videoHandler.addVideo(video)
    return render_template("complete.html",variable=video.path)

@app.route("/generateTextFile")
def generateTextFile():
    video=videoHandler.videos[0]
    videoHandler.splitVideo(video)
    videoHandler.compareImages()
    videoHandler.generateTextFile()
    return render_template('textGenerated.html')

if __name__ == '__main__':
    app.run(debug=True)

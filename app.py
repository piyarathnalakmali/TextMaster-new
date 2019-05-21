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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/uploadVideo-storage')
def uploadVideo_storage():
    return render_template('uploadVideo_storage.html')

@app.route('/uploadVideo-link')
def uploadVideo_link():
    return render_template('uploadVideo_link.html')

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
    return render_template("generateText.html",variable=video.path)

@app.route('/uploadByLink' , methods = ["POST"])
def uploadByLink():
    #url = request.args['url']
    r = request.get(url)
    print(request)
    with app.open_instance_resource('downloaded_file', 'wb') as f:
        f.write(r.content)
    return render_template("generateText.html",variable=video.path)

@app.route("/generateTextFile" , methods=["POST"])
def generateTextFile():
    text = request.form['text']
    print(text)
    video=videoHandler.getVideoByName(text)
    videoHandler.splitVideo(video)
    videoHandler.compareImages()
    text=videoHandler.generateTextFile()
    return render_template('editText.html',variable=text)

@app.route("/editTextFile" , methods=["POST"])
def editTextFile():
    editedText=request.form['text']
    print (editedText)
    f= open("Text.txt","w")
    f.write(editedText)
    f.close()
    return editedText

if __name__ == '__main__':
    app.run(debug=True)

import os
import codecs
import requests
import pytube
import random
from flask import Flask , render_template , request , Response,send_file
from pytube import YouTube
from Video import Video
from VideoHandler import VideoHandler
from VideoCamera import VideoCamera
from flask_sockets import Sockets
app=Flask(__name__)
sockets = Sockets(app)
videoHandler = VideoHandler()
global webSocket
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
    id= random.randint(1,1000)
    return render_template('home.html',user_id=id)

@sockets.route('/echo')
def echo_socket(ws):
    webSocket = ws;
    while True:
        message = ws.receive()
        print(message)
        for i in range(4):
            ws.send("Charith");


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
    user_id= request.form['user_id']
    target=os.path.join(APP_ROOT, 'videos/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename=file.filename
        destination = "/".join([target,filename])
        file.save(destination)
        video = Video(filename,destination,user_id)
        videoHandler.addVideo(video)
    return render_template("generateText.html",variable=video.user)

@app.route('/uploadByLink' , methods = ["POST"])
def uploadByLink():
    #user_id= request.form['user_id']
    target=os.path.join(APP_ROOT, 'videos/')
    if not os.path.isdir(target):
        os.mkdir(target)
    url = request.form['url']
    yt = YouTube(url)
    filename=yt.title
    destination="/".join([target,filename])
    stream=yt.streams.first()
    stream.download(target)
    video = Video(filename,destination)
    videoHandler.addVideo(video)
    return render_template("generateText.html",variable=video.path)

@app.route("/generateTextFile" , methods=["POST"])
def generateTextFile():
    user_id = request.form['user_id']
    print(user_id)
    video=videoHandler.getVideoByUserId(user_id)
    name=video.name;
    print(name);
    print(video);
    videoHandler.splitVideo(video)
    videoHandler.compareImages()
    text = videoHandler.generateTextFile(video)
    print(text)
    return render_template('editText.html', variable=user_id, name=name, textData = text)

@app.route("/editTextFile" , methods=["POST"])
def editTextFile():
    editedText=request.form['text']
    print (editedText)
    f= open("Text.txt","w")
    f.write(editedText)
    f.close()
    return send_file('Text.txt',mimetype='text/plain',as_attachment=True)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed',methods=['GET'])
def video_feed():
    video = videoHandler.getVideoByUserId(request.args.get("id"))
    return send_file(video.path,as_attachment=True)

@app.route('/video_text',methods=['GET'])
def video_text():
    textId = request.args.get("id")
    return send_file("text/"+textId+".vtt", attachment_filename=textId+".vtt", mimetype='text/vtt', as_attachment=True)

if __name__ == '__main__':
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
    app.run(debug=True)

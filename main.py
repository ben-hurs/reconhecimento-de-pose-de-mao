from flask import Flask, render_template, Response
import cv2
from reconhecimento_mao import videoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(reconhecimento_mao):
    while True:
        frame = reconhecimento_mao.get_frames()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame 
            + b'\r\n\r\n')
        
@app.route('/aplicacao')
def aplicacao():
    return Response(gen(videoCamera()),
           mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

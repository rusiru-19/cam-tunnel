import cv2
from flask import Flask, Response
from pyngrok import ngrok


app = Flask(__name__)
camera = cv2.VideoCapture(0)

port1 = 8080
ngrok.set_auth_token("") # <== put ur dammn ngrok autho token
url = ngrok.connect(port1)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def cleanup_camera(_):
    print("Cleaning up camera...")
    camera.release()

app.teardown_appcontext(cleanup_camera)

if __name__ == '__main__':
    try:
        app.run(port=8080, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_camera(None) 

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import ngl

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nglusername = request.form['nglusername']
        message = request.form['message']
        count = int(request.form['count'])
        use_proxy = request.form.get('use_proxy') == 'on'

        # Run the ngl function in a separate thread to avoid blocking
        socketio.start_background_task(ngl.ngl, nglusername, message, count, use_proxy, socketio)
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

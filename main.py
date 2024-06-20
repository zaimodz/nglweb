from flask import Flask, render_template, request, redirect, url_for
import ngl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nglusername = request.form['nglusername']
        message = request.form['message']
        count = int(request.form['count'])
        use_proxy = request.form.get('use_proxy') == 'on'
        
        ngl.ngl(nglusername, message, count, use_proxy)
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

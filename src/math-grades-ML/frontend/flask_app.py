from flask import Flask, request, render_template
import time

start = time.time()

app = Flask(__name__, static_url_path='/', 
                      static_folder='static',
                      template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html', v='1.a')

@app.route('/send', methods=['POST'])
def send():
    data = request.form
    for k, v in data.items():
        print(k, v)
    return "OK"
    
@app.route('/test')
def test():
    return f"Hello from Test! {(time.time()-start)/60:.2f}"
    

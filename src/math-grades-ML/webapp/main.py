from flask import Flask, request, render_template, send_file
import time
import csv

fieldnames = [
  "OutMarker",
  "famsize",
  "Pstatus",
  "Medu",
  "Fedu",
  "Mjob",
  "Fjob",
  "guardian",
  "studytime",
  "schoolsup",
  "famsup",
  "paid",
  "activities",
  "nursery",
  "higher",
  "internet",
  "freetime",
  "health"
]


app = Flask(__name__, static_url_path='/', 
                      static_folder='static',
                      template_folder='templates')

app_version = '1.0'
CSV_FILE_NAME = app.root_path + '/data/form_data.csv';
                      
@app.route('/')
def index():
    return render_template('index.html', v=app_version)

@app.route('/form')
def form():
    return render_template('form.html', v=app_version)

@app.route('/predict')
def predict():
    return render_template('predict.html', v=app_version)

@app.route('/send', methods=['POST'])
def send():
    data = request.form
    new_row_data = [data[k] for k in data]
    
    # Если файл данных новый, то нужно записать заголовок
    try:
        with open(CSV_FILE_NAME, 'x', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass
    
    # Записываем данные
    with open(CSV_FILE_NAME, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writerow(data)
    
    return render_template('thanks.html', v=app_version)

@app.route('/download_data')
def download_report():
    # Use send_file to prompt a download
    return send_file(CSV_FILE_NAME, as_attachment=True)
    

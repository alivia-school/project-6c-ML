# Подключаем библиотеки
from flask import Flask, request, render_template, send_file
import csv
import tensorflow as tf
from dataset import check_row, processing_row, dataset_values

app_version = '1.0'
app = Flask(__name__, static_url_path='/', 
                      static_folder='static',
                      template_folder='templates')

# Загрузка обученной модели
model = tf.keras.models.load_model(app.root_path + '/data/model.h5')

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
    data = request.form.to_dict()
    
    if not check_row(data):
        return "Bad post data"
                
    fieldnames = list(dataset_values.keys())

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
    
    
@app.route('/result', methods=['POST'])
def result():
    data = request.form.to_dict()
    row = [list(processing_row(data).values())]    

    predictions = model.predict(row, verbose=False)
    result_number = predictions[0][0]
    
    if result_number < 2.2:
        result =  "У вас высокая вероятность получить неудовлетворительную оценку"
    elif result_number < 3.2:       
        result =  "У вас есть вероятность получить \"три\""
    elif result_number < 4.2:       
        result =  "У вас есть вероятность получить \"четыре\""
    elif result_number < 4.5:       
        result =  "У вас есть вероятность получить \"пять\""
    else:       
        result =  "У вас высока вероятность получить \"пять\""
        
    return render_template('result.html', v=app_version, result=result)
 
        


    

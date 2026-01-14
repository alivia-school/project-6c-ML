# Подключаем библиотеки
from flask import Flask, request, render_template, send_file
import csv
import tensorflow as tf
from dataset import check_row, processing_row, dataset_values


# Версия приложения
app_version = '1.0'

# Создаем веб приложение
app = Flask(__name__, static_url_path='/', 
                      static_folder='static',
                      template_folder='templates')

# Загрузка обученной модели
model = tf.keras.models.load_model(app.root_path + '/model/model.h5')

        

# Функция для маршрута '/'
# Основная страница, отображается информация о проекте и кнопки сбора данных и прогноза
@app.route('/')
def index():
    return render_template('index.html', v=app_version)


# Функция для маршрута '/form'
# Страница формы сбора данных для обучения
@app.route('/form')
def form():
    return render_template('form.html', v=app_version)


# Функция для маршрута '/predict'
# Страница формы для прогноза
@app.route('/predict')
def predict():
    return render_template('predict.html', v=app_version)


# Функция для маршрута '/send'
# Сюда отсылается данные со страницы '/form'
# Выполняется проверка и сохранение переданных данных в файл
@app.route('/send', methods=['POST'])
def send():
    data = request.form.to_dict()
    
    # Проверка данных формы
    if not check_row(data):
        return "Bad post data"
                
    fieldnames = list(dataset_values.keys())
   
    csv_file_name = app.root_path + '/data/form_data.csv';
   
    # Если файл данных новый, то нужно записать заголовок
    try:
        with open(csv_file_name, 'x', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass
    
    # Записываем данные
    with open(csv_file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writerow(data)
    
    return render_template('thanks.html', v=app_version)
    

# Функция для маршрута '/result'
# Сюда отсылается данные со страницы '/predict'    
# Выполняется проверка и перевод в параметры для модели переданных данных, 
# затем затем результат прогноз на их основе отсылается пользователю
@app.route('/result', methods=['POST'])
def result():
    
    # Проверка и перевод данных формы в параметры для модели 
    row = processing_row(request.form.to_dict())    
    if not row:
        return 'Bad post data'
    
    # Прогноз    
    prediction = model.predict([list(row.values())], verbose=False)[0][0]
    
    if prediction < 2.2:
        result =  'У вас есть вероятность получить неудовлетворительную оценку'
    elif prediction < 3.2:       
        result =  'У вас есть вероятность получить "три"'
    elif prediction < 4.1:       
        result =  'У вас есть вероятность получить "четыре"'
    elif prediction < 4.5:       
        result =  'У вас есть вероятность получить "пять"'
    else:       
        result =  'У вас высокая вероятность получить "пять"'
        
    return render_template('result.html', v=app_version, result=result)
 
        


    

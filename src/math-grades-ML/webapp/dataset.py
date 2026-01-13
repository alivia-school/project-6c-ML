# Подключаем библиотеки
import pandas as pd

# Описание структуры набора данных и соответствия данных и значений параметров для модели
dataset_values = {
  'famsize': {'LE3': 0, 'GT3': 1},
  'Pstatus': {'A': 0, 'T': 1},
  'Medu': {'0': 0, '1': 0.25, '2': 0.5, '3': 0.75, '4': 1},
  'Fedu': {'0': 0, '1': 0.25, '2': 0.5, '3': 0.75, '4': 1},  
  'Mjob': {'teacher': 0, 'health': 0.25, 'services': 0.5, 'at_home': 0.75, 'other': 1},
  'Fjob': {'teacher': 0, 'health': 0.25, 'services': 0.5, 'at_home': 0.75, 'other': 1},
  'guardian': {'mother': 0, 'father': 0.5, 'other': 1},
  'studytime':  {'1': 0, '2': 0.33333, '3': 0.66666, '4': 1},  
  'schoolsup': {'no': 0, 'yes': 1},
  'famsup': {'no': 0, 'yes': 1},
  'paid': {'no': 0, 'yes': 1},
  'activities': {'no': 0, 'yes': 1},
  'nursery': {'no': 0, 'yes': 1},
  'higher': {'no': 0, 'yes': 1},
  'internet': {'no': 0, 'yes': 1},  
  "freetime": {'1': 0, '2': 0.25, '3': 0.5, '4': 0.75, '5': 1},
  "health": {'1': 0, '2': 0.25, '3': 0.5, '4': 0.75, '5': 1},  
  'OutMarker':  {'2': 2, '3': 3, '4': 4, '5': 5},
}
  

# Функция перевода набора данных в параметры для модели   
def processing(dataset):
    with pd.option_context("future.no_silent_downcasting", True):
        dataset = dataset.replace(dataset_values).astype("float32")
    return dataset

# Функция перевода записи данных в параметры для модели и проверка корректности данных
# Используется для данных переданных через форму прогноза на сайте
def processing_row(row):
    new_row = {}
    try:
        for key, value in dataset_values.items():
            if not key in ['OutMarker']:
                new_row[key] = dataset_values[key][str(row[key])]
    except Exception as e:
        return None
        
    return new_row

    
# Функция проверка корректности данных
# Например используется для данных переданных через форму сбора данных на сайте
def check_row(row):   
    try:
        for key, value in row.items():
            v = dataset_values[key][str(value)]
    except Exception as e:
        return False
        
    return True
    
    
    
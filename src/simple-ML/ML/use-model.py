# Подключаем библиотеки
import tensorflow as tf

# Загрузка обученной модели
model = tf.keras.models.load_model('function-model.h5')
 
# Получяем строку с числом и переводим его в число
x = int(input("Введите x: "))

# Просим нашу модель предсказать результат для x
y = model.predict([x], verbose=False)[0][0]
  
# Выводим результат
print ("Результат:", y)


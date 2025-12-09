# Подключаем библиотеки
import tensorflow as tf
import numpy as np

# Тренировочные данные
X = np.array([1, 2, 3, 4 ]) # Входные данные
y = np.array([5, 7, 9, 11]) # Выходные данные (результат функции y = 2x + 3 для данных из X)
# Тестовые данные
X_test = np.array([10, 11, 12]) # Входные данные
y_test = np.array([23, 25, 27]) # Выходные данные (результат функции y = 2x + 3 для данных из X_test)

# Создаём модель для предсказания результата простого линейного уравнения
model = tf.keras.Sequential([
    # Слой Dense (y = Wx + b), один нейрон и одни входные данные
    tf.keras.layers.Dense(units=1, input_shape=[1], use_bias = True) 
])

# Собираем модель
model.compile(optimizer='adam',loss='mean_squared_error')

# Посмотрим начальные случайные веса до обучения
print("Начальные веса (до обучения):")
W, b = model.get_weights()
print(f"W = {W[0][0]:.8f}, b = {b[0]:.8f}") 

# Для того чтобы смотреть прогресс обучения, разделим обучение на 5 этапов
for i in range(5):
    # Обучаем модель
    model.fit(X, y, epochs=3000, verbose=False)
    
    # Посмотрим веса после каждого этапа
    print(f"\nОбученные веса (этап {i+1}):")
    W, b = model.get_weights()
    print(f"W = {W[0][0]:.8f}, b = {b[0]:.8f}")
    
# Тестируем модель, чем меньше loss тем лучше. Идеал loss = 0
loss = model.evaluate(X_test, y_test, verbose=False)
print(f'\nРезультат тестирования loss = {loss:.4f}')

# Использование модели. 
# Получяем строку с числом и переводим его в число
x = int(input("\nВведите x: "))

# Просим нашу модель предсказать результат для x
y = model.predict([x], verbose=False)[0][0]
  
# Выводим результат
print ("Результат:", y)

# Сохраним созданную и обученную модель в файл для дальнейшего использования 
model.save('function-model.h5')


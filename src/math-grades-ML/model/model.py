# Подключаем библиотеки
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from dataset import processing

# Загружаем данные
df = pd.read_csv('data/dataset.csv', sep=';')

# Переводим данные в параметры для модели
df = processing(df)

# Берем из данных входные параметры(признаки)
X = df.drop('OutMarker', axis=1)
# Берем из данных целевую переменную(метка)
y = df['OutMarker']

# Разделение на тренировочные и тестовые данные
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Описание модели
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Компиляция модели
model.compile(
    optimizer="adam",
    loss="mse",  # среднеквадратичная ошибка для регрессии
)

# Обучение модели
model.fit(
    X_train, y_train,
    epochs=1800,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=True
)

# Тестирование модели
test_loss = model.evaluate(X_test, y_test, verbose=False)
print(f"Test loss: {test_loss:.4f}")

# Сохраним созданную и обученную модель в файл для дальнейшего использования 
model.save('data/model.h5')





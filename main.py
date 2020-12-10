import csv
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

# carrega linha a linha
def readFile(filename):
    arr = []
    with open(filename, newline='') as arquivo:
        dados = csv.reader(arquivo, delimiter=';')
        next(dados)
        for linha in dados:
            arr.append(linha)
    return arr

# cria dataset treino(campo)
def criar_dataset(dados, inicio, fim=None):
    if(fim is None):
        dados = dados[inicio:len(dados)]
    else:
        dados = dados[inicio:fim]

    dados_x = list(map(lambda x: list(map(lambda y: int(y), x[3:9])), dados))
    if len(dados[0]) == 9:
        dados_y = list(map(lambda x: 0, dados))
    else:
        dados_y = list(map(lambda x: 1 if(x[9] == 'Atacante') else 0, dados))
    return tf_set(dados_x, dados_y)


def preprocess(x, y):
    x = tf.cast(x, tf.float16) / 100

    return x, y


def tf_set(xs, ys, n_classes=2):
    ys = tf.one_hot(ys, depth=n_classes)
    return tf.data.Dataset.from_tensor_slices((xs, ys)) \
        .map(preprocess)\
        .batch(128)


jogadores = readFile('datasets/jogadores.csv')
jogadores_resultantes = readFile('datasets/validacao.csv')
N_TREINO = int(len(jogadores)*80/100)

jogadores_treino = criar_dataset(jogadores, 0, N_TREINO)
jogadores_teste = criar_dataset(jogadores, N_TREINO)
jogadores_resultantes = criar_dataset(jogadores_resultantes, 0)

model = keras.Sequential([
    keras.layers.Dense(units=2, activation='sigmoid')
])

model.compile(optimizer='sgd',
              loss=tf.losses.BinaryCrossentropy(),
              metrics=['accuracy'])
epochs = 10
steps_per_epoch = 500
validation_steps = 2
history = model.fit(
    jogadores_treino.repeat(),
    epochs=epochs,
    steps_per_epoch=steps_per_epoch,
    validation_data=jogadores_teste.repeat(),
    validation_steps=validation_steps,
    batch_size=128
)

predictions = model.predict(jogadores_teste)

legenda = ['Defensor', 'Atacante']
i = 1
if not os.path.exists('resultados'):
    os.makedirs('resultados')
f = open("resultados/classes_testes_" + str(epochs) + "_" + str(steps_per_epoch) +
         "_" + str(validation_steps) + ".txt", "w")
f.write("CICLOS = " + str(epochs) + " || PASSOS POR CICLO = " +
        str(steps_per_epoch) + " || PASSOS DE VALIDACAO = " + str(validation_steps) + " || PRECISAO = \n")
f.write("===================================================================================\n")
for element in predictions:
    f.write(str(i) + ' = ' + legenda[np.argmax(element)] + "\n")
    i += 1
f.close()

import numpy as np
import tensorflow as tf
import csv


def readFile(filename):
    arr = []
    with open(filename, newline='') as arquivo:
        dados = csv.reader(arquivo, delimiter=';')
        next(dados)
        for linha in dados:
            arr.append(linha)
    return arr


def criar_dataset(dados, inicio, fim=None):
    if(fim is None):
        dados = dados[inicio:len(dados)]
    else:
        dados = dados[inicio:fim]

    dados_x = list(map(lambda x: x[3:9], dados))
    dados_y = list(map(lambda x: 1 if(x[9] == 'Atacante') else 0, dados))

    return tf_set(dados_x, dados_y)


def preprocess(x, y):
    x = tf.cast(x, tf.float32) / 100
    return x, y


def tf_set(xs, ys, n_classes=2):
    ys = tf.one_hot(ys, depth=n_classes)
    return tf.data.Dataset.from_tensor_slices((xs, ys)) \
        .map(preprocess) \
        .shuffle(len(ys)) \
        .batch(128)


jogadores = readFile('datasets/jogadores.csv')
jogadores_resultantes = readFile('datasets/validacao.csv')
N_TREINO = int(len(jogadores)*80/100)

jogadores_treino = criar_dataset(jogadores, 0, N_TREINO)
jogadores_teste = criar_dataset(jogadores, N_TREINO)

print(jogadores_treino)

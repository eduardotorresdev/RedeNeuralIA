import csv


class Jogador(object):
    def __init__(self, dados):
        self.id = dados[0]
        self.idade = dados[1]
        self.altura = dados[2]
        self.tecnica = dados[3]
        self.passe = dados[4]
        self.chute = dados[5]
        self.forca = dados[6]
        self.velocidade = dados[7]
        self.drible = dados[8]
        self.classe = None if len(dados) != 10 else dados[9]

    def __str__(self):
        return ("{" +
                "\n id: " + self.id +
                ",\n idade: " + self.idade +
                ",\n altura: " + self.altura +
                ",\n tecnica: " + self.tecnica +
                ",\n passe: " + self.passe +
                ",\n chute: " + self.chute +
                ",\n forca: " + self.forca +
                ",\n velocidade: " + self.velocidade +
                ",\n drible: " + self.drible +
                ",\n classe: " + (self.classe or 'none') +
                "\n}")


def readFile(filename):
    arr = []
    with open(filename, newline='') as arquivo:
        dados = csv.reader(arquivo, delimiter=';', skipinitialspace=True)
        next(dados)
        for linha in dados:
            arr.append(Jogador(linha))
    return arr


jogadores = readFile('datasets/jogadores.csv')
jogadores_ideais = readFile('datasets/validacao.csv')

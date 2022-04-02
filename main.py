import csv
from collections import Counter
import statistics


class Jogo:
    def __init__(self, nome, media, moda, desvio, mediana, quantidade, vendas):
        self.nome = nome
        self.media = media
        self.moda = moda
        self.desvio = desvio
        self.mediana = mediana
        self.quantidade = quantidade
        self.vendas = vendas


class Game:
    def __init__(self, nome, media, vendas):
        self.nome = nome
        self.media = media
        self.vendas = vendas

def moda(sample):
        c = Counter(sample)
        return [k for k, v in c.items() if v == c.most_common(1)[0][1]]



def variancia(vish):
    data = list(map(int, vish))
    mean = sum(data) / len(data)
    variance = sum([((x - mean) ** 2) for x in data]) / len(data)
    res = variance ** 0.5
    return res

def median(aux1):
    data = list(map(int, aux1))
    n = len(data)
    data.sort()
    return data[round(n / 2)]

def dupRemove(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res


for graph in range(5, 250):

    critic_score_sum = 0
    critic_score_counter = 0

    totalSales = 0

    porcentagem = 0

    porcentCount = 0

    lista = []
    listaNotas = []

    listaJogos = []

    listaGames = []

    gameOver = []

    previous = ""

    lineCount = 0

    grafico = 0



    with open('empresa_convert.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if lineCount == 0:
                lineCount += 1
            else:
                if row[10]:
                    if row[4] == previous:
                        lista.append(row[14])
                        listaNotas.append(row[10])
                        critic_score_sum += int(row[10])
                        totalSales += float(row[9])
                        critic_score_counter += 1
                        newJogo = Game(row[0], int(row[10]), float(row[9]))
                        listaGames.append(newJogo)
                        if newJogo.nome in listaGames:
                            listaGames.pop(len(listaGames) - 1)
                    else:
                        if critic_score_counter != 0:
                            totalSales = totalSales / critic_score_counter
                            if critic_score_counter > 1.5*graph:
                                tempListMedia = []
                                tempListValor = []

                                listaGames.sort(key=lambda x: x.media, reverse=False)

                                for i in range(0, graph):
                                    tempListMedia.append(listaGames[i].nome)
                                listaGames.sort(key=lambda x: x.vendas, reverse=True)

                                for i in range(0, graph):
                                    tempListValor.append(listaGames[i].nome)
                                listaGames.clear()

                                _auxset = set(tempListValor)
                                c = [x for x in tempListMedia if x in _auxset]
                                c = dupRemove(c)
                                porcentagem += (len(c) / graph)*100
                                porcentCount += 1

                                jogo = Jogo(previous, round(critic_score_sum / critic_score_counter), moda(listaNotas)[0], round(variancia(listaNotas)), median(listaNotas), critic_score_counter, totalSales)
                                listaJogos.append(jogo)

                        critic_score_sum = 0
                        critic_score_counter = 0
                        totalSales = 0
                        lista.clear()
                        listaNotas.clear()
                        previous = row[4]

                        lista.append(row[14])
                        listaNotas.append(row[10])

                        critic_score_sum += int(row[10])
                        critic_score_counter += 1

                else:
                    continue

    with open('casoMedio.txt', 'a') as f:
        f.writelines(f'({graph},{round(porcentagem / porcentCount, 2)}),')

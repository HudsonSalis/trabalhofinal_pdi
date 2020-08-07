# -*- coding: utf-8 -*-

import sys
import numpy as np

# Checando os argumentos de linha de comando
if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f'Argument:{i}: {arg}')

# Abrir os arquivos de entrada e de saída
entrada = open(sys.argv[1], "r+")
saida = open(sys.argv[2], "w+")
linha = entrada.readline() # P1
linha = entrada.readline() # Comentário
linha = entrada.readline() # Dimensões da imagem
dimensoes = linha.split() # Lista com as dimensões
largura = int(dimensoes[0])
altura = int(dimensoes[1])
dimensoes = np.asarray(dimensoes, dtype=int)

linhas = entrada.readlines()
linhas = [x.strip() for x in linhas]


def concatenate_list_data(list):
    result = ''
    for element in list:
        result += str(element)
    return result



longstring = concatenate_list_data(linhas)
image = np.array(list(longstring))
image = np.reshape(image, [dimensoes[1], dimensoes[0]])
image = image.astype(int)

#Elemento Estruturante 3x3
#elemento = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]


#Elemento Estruturante 5x5
#elemento = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]


#Elemento Estruturante 7x7
#elemento = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
#            [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]

#Elemento Estruturante 9x9
elemento = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]

#Array numpy do elemento estruturante
elemento = np.asarray(elemento)

#Pegar pixel posição pixel central
es = int((len(elemento) - 1) / 2)

#escrevendo a imagem cópia
saida.write("P1\n")
saida.write("#Criado por Hudson\n")
saida.write(str(largura))
saida.write(" ")
saida.write(str(altura))
saida.write("\n")

#Fazer cópia da imagem original
image2 = image.copy()

for px in range(es, len(image)-es):
    for py in range(es, len(image[1])-es):
        if image[px][py] == 0:
            for ex in range(len(elemento)):
                for ey in range(len(elemento[1])):
                    if elemento[ex][ey] == 1:
                        image2[px - es + ex][py - es + ey] = 0

print(image2)

for linha in range(len(image2)):
    for coluna in range(len(image2[1])):
        saida.write(str(image2[linha][coluna]))
    saida.write("\n")


# fechar os dois arquivos.
entrada.close()
saida.close()

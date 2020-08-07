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
dimensoes = np.asarray(dimensoes, dtype=int) # Converte a lista para um array

linhas = entrada.readlines()
linhas = [x.strip() for x in linhas]


def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result


longstring = concatenate_list_data(linhas)
image = np.array(list(longstring))
image = np.reshape(image, dimensoes)
image = image.astype(int)

#Edge Detection
#kernel = [[1, 0, -1], [0, 0, 0], [-1, 0, 1]]
#kernel = np.asarray(kernel)

#kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
#kernel = np.asarray(kernel)

kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
kernel = np.asarray(kernel)

ks = int((len(kernel) - 1) / 2)

#escrevendo a imagem cópia
saida.write("P1\n")
saida.write("#Criado por Hudson\n")
saida.write(str(largura-(ks*2)))
saida.write(" ")
saida.write(str(altura-(ks*2)))
saida.write("\n")

#fazer a transformação
for i in range(ks, len(image)-ks):
    for j in range(ks, len(image[1])-ks):
        sum = 0
        for ki in range(len(kernel)):
            for kj in range(len(kernel[1])):
                sum = sum + (image[i - ks + ki][j - ks + kj] * kernel[ki][kj])
        if sum < 0:
            sum = 0
        if sum > 1:
            sum = 1
        sum = str(sum)
        saida.write(sum)
        saida.write("\n")


# fechar os dois arquivos.
entrada.close()
saida.close()

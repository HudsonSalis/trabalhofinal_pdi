# *-* coding: utf:8 -*-

import sys
import numpy as np
import math

# Checando os argumentos de linha de comando
if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f'Argument:{i}: {arg}')


# Abrir os arquivos de entrada e de saída
entrada = open(sys.argv[1], "r+")
saida = open(sys.argv[2], "w+")


linha = entrada.readline() #P3
linha = entrada.readline() #Comentário
linha = entrada.readline() #Dimensões
dimensoes = linha.split()
largura = int(dimensoes[0])
altura = int(dimensoes[1])
linha = entrada.readline() #Valor fixo
linha = entrada.readlines() #Ler o restante do arquivo e grava como lista

#converter de lista para array
imagem = np.asarray(linha, dtype=int)
#reshape
imagem = np.reshape(imagem, (altura, largura, 3))

#escrevendo a imagem cópia
saida.write("P3\n")
saida.write("#Criado por Hudson\n")
saida.write(str(largura))
saida.write(" ")
saida.write(str(altura))
saida.write("\n")
saida.write("255\n")

#fazer a cópia
for i in range(len(imagem)):
    for j in range(len(imagem[1])):
        for k in range(3):
            sum = int((math.log(1 + (imagem[i][j][k]/255)))*255)
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")

#fechar os dois arquivos.
entrada.close()
saida.close()

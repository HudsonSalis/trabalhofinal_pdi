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
#print(imagem)
#print(imagem.shape)
#print(len(imagem))
#print(len(imagem[1]))

#Sobel
kernelx = [[-1,0,1],[2,0,-2],[1,0,-1]]
kernelx = np.asarray(kernelx)
kernely = [[1,2,1],[0,0,0],[-1,-2,-1]]
kernely = np.asarray(kernely)
print(kernelx)
print(kernely)
ks = int((len(kernelx)-1)/2)
#print(ks)
threshold = 200


#escrevendo a imagem cópia
saida.write("P3\n")
saida.write("#Criado por Hudson\n")
saida.write(str(largura-(ks*2)))
saida.write(" ")
saida.write(str(altura-(ks*2)))
saida.write("\n")
saida.write("255\n")


#fazer a transformação
for i in range(ks, len(imagem)-ks):
    for j in range(ks, len(imagem[1])-ks):
        for k in range(3):
            sumx = 0
            sumy = 0
            for ki in range(len(kernelx)):
                for kj in range(len(kernelx[1])):
                    sumx = sumx + (imagem[i-ks+ki][j-ks+kj][k]*kernelx[ki][kj])
                    sumy = sumy + (imagem[i-ks+ki][j-ks+kj][k]*kernely[ki][kj])
            sumxy = math.sqrt((sumx**2)+(sumy**2))
            #Threshold
            sum = max(sumxy, threshold)
            sum = int(sum) if sum != threshold else 0
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")

#fechar os dois arquivos.
entrada.close()
saida.close()

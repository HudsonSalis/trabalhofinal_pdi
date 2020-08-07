# -*- coding: utf-8 -*-
import numpy as np

entrada = open("star.pbm", "r+")
saida = open("star_fechamento_3x3.pbm", "w+")

linha = entrada.readline() # P1
linha = entrada.readline() # Comentário
linha = entrada.readline() # Dimensões da imagem
dimensoes = linha.split() # Lista com as dimensões
largura = int(dimensoes[0])
altura = int(dimensoes[1])
dimensoes = np.asarray(dimensoes, dtype=int) # Converte a lista para um array

linhas = entrada.readlines() # lê todo o restante do arquivo
linhas = [x.strip() for x in linhas] # remove o \n do final de todas as linhas


def concatenate_list_data(list):
    result = ''
    for element in list:
        result += str(element)
    return result


#concatena todos os elementos em uma única string
longstring = concatenate_list_data(linhas)
#converte a string longa para um array de uma dimensão
image = np.array(list(longstring))
#muda a forma do array de [altura*largura, 1] para [altura, largura]
image = np.reshape(image, [dimensoes[1], dimensoes[0]])
#converte a matriz para inteiro
image = image.astype(int)

'''
image agora é um array de [altura, largura] e pode ser  usado nas estruturas de repetição 
como nos outros códigos (ppm e pgm).
'''
#print(image)
#print(image.shape)


#Elemento Estruturante 3x3
elemento = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


#Elemento Estruturante 5x5
#elemento = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]


#Elemento Estruturante 7x7
#elemento = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
#            [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]

#Elemento Estruturante 9x9
#elemento = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1],
#            [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1],
#            [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]



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

#Fazer a dilatação
for px in range(es, len(image)-es):
    for py in range(es, len(image[1])-es):
        if image[px][py] == 1:
            for ex in range(len(elemento)):
                for ey in range(len(elemento[1])):
                    if elemento[ex][ey] == 1:
                        image2[px - es + ex][py - es + ey] = 1

print(image2)
print("\n")

#Fazer cópia da imagem dilatada
image3 = image2.copy()

# Fazer a erosão
for px in range(es, len(image2)-es):
    for py in range(es, len(image2[1])-es):
        if image2[px][py] == 0:
            for ex in range(len(elemento)):
                for ey in range(len(elemento[1])):
                    if elemento[ex][ey] == 1:
                        image3[px - es + ex][py - es + ey] = 0

print(image3)

for linha in range(len(image3)):
    for coluna in range(len(image3[1])):
        saida.write(str(image3[linha][coluna]))
    saida.write("\n")

# fechar os dois arquivos.
entrada.close()
saida.close()

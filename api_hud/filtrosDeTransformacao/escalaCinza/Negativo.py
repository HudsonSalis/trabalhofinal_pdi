# *-* coding: utf:8 -*-
import numpy as np
import sys

if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f'Argument:{i}: {arg}')


# Abrir os arquivos de entrada e de saída
entrada = open(sys.argv[1], "r+")
saida = open(sys.argv[2], "w+")

linha = entrada.readline() #P2
linha = entrada.readline() #comentário
linha = entrada.readline() #Dimensões
dimensoes = linha.split()
largura = dimensoes[0]
altura = dimensoes[1]
linha = entrada.readline() #Valor fixo

linha = entrada.readlines() # ler o restante do arquivo e grava como lista

#converter de lista para array
imagem = np.asarray(linha, dtype=int)

#escrevendo a imagem cópia
saida.write("P2\n")
saida.write("#Criado por Hudson\n")
saida.write(largura)
saida.write(" ")
saida.write(altura)
saida.write("\n")
saida.write("255\n")

#fazer a transformação de intesidade (negativo)
for i in range((len(imagem))):
    n = 255 - imagem[i]
    n = str(n)
    saida.write(n)
    saida.write("\n")


#fechar os dois arquivos
entrada.close()
saida.close()
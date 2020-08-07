# *-* coding: utf:8 -*-
import sys
import numpy as np

# Convertindo uma imagem colorida PPM para escala de cinza PGM

# Checando os argumentos de linha de comando
if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f'Argument:{i}: {arg}')


# Abrir os arquivos de entrada e de saída
entrada = open(sys.argv[1], "r+")
saida = open(sys.argv[2], "w+")

# Fazer o Processamento Digital de Imagens
linha = entrada.readline() #P3
linha = entrada.readline() #Comentário
linha = entrada.readline() #Dimensões
dimensoes = linha.split()
linha = entrada.readline() # Valor Fixo
dimensoes = np.array(dimensoes, dtype=int)

linhas = entrada.readlines() # Lê o arquivo até o final
#converter para uma matriz de inteiros
image = np.array(list(linhas)) #array de uma dimensão
image = np.reshape(image, [dimensoes[1], dimensoes[0], 3]) #converte a array em uma matriz com as dimensões da imagem
image = image.astype(int)

#Escreve o arquivo de saída
saida.write('P3\n')
saida.write('#Criado por Hudson\n')
largura = dimensoes[0]
altura = dimensoes[1]
saida.write(str(largura))
saida.write(' ')
saida.write(str(altura))
saida.write('\n')
saida.write('255\n')

#fazer a cópia
for i in range(len(image)):
    for j in range(len(image[1])):
        for k in range(3):
            sum = 255 - image[i][j][k]
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")


# Fechar os arquivos de entrada e de saída
entrada.close()
saida.close()

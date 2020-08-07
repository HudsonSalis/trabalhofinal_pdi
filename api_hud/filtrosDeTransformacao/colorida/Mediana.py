# *-* coding: utf:8 -*-

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

#Mediana(BoxBlur)
kernel = np.ones((3, 3))
kernel = np.asarray(kernel)/9

print(kernel)

ks = int((len(kernel) - 1) / 2)
#print(ks)

#Escreve o arquivo de saída
saida.write('P3\n')
saida.write('#Criado por Hudson\n')
largura = dimensoes[0]
altura = dimensoes[1]
saida.write(str(largura-(ks*2)))
saida.write(' ')
saida.write(str(altura-(ks*2)))
saida.write('\n')
saida.write('255\n')

#fazer a cópia
for i in range(ks, len(image)-ks):
    #print((round((i*100)/(len(image)-ks))))
    for j in range(ks, len(image[1])-ks):
        for k in range(3):
            sum = 0
            for ki in range(len(kernel)):
                for kj in range(len(kernel[1])):
                    sum = sum + (image[i - ks + ki][j - ks + kj][k] * kernel[ki][kj])
            sum = int(sum)
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")



#fechar os dois arquivos.
entrada.close()
saida.close()

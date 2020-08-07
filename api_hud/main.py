
import sys
import os
import shutil
import subprocess
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from win32api import GetSystemMetrics
from PyQt5.QtGui import QDesktopServices,QTransform
from PyQt5.QtWidgets import QLabel


porcentagemProgresso = 0
imagemResultado = 'imagensResultado/imagemTransformada'
extensaoImagemResultado = '.ppm'
listaFiltrosUsados = []

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Processamento Digital de Imagens - IFTM")
        self.setWindowIcon(QIcon("imagens/netero.jpg"))
        self.setGeometry(450, 150, 800, 600)
        self.setStyleSheet("Background-Color:	#4682B4;")
    
        self.initUI()
        self.show()

    'Chamar métodos que criam a interface'
    def initUI(self):
        self.criarWidgets()
        self.gerarLayouts()

    'Cria os widgets que encorporam o Menu e widgets que executaram ações'
    def criarWidgets(self):
        # Criar a barra de menu
        self.barraMenu = self.menuBar()

        # Criar menus
        self.menuArquivo = self.barraMenu.addMenu("&Arquivo")
        self.menuTransformacao = self.barraMenu.addMenu("&Transformações")
        self.menuSobre = self.barraMenu.addMenu("So&bre")
        

        # Crias as actions
        self.opcaoAbrir = self.menuArquivo.addAction("A&brir")
        self.opcaoAbrir.triggered.connect(self.abrirImagem)
        self.opcaoAbrir.setShortcut("Ctrl+A")

        self.opcaoRecente = self.menuArquivo.addMenu("Abrir &Recente")
        self.abrirRecente = self.opcaoRecente.addAction("arquivos...")
        self.abrirRecente.setDisabled(True)

        self.opcaoSalvarComo = self.menuArquivo.addAction("&Salvar como")
        self.opcaoSalvarComo.triggered.connect(self.salvarImagemComo)
        self.opcaoSalvarComo.setShortcut("Ctrl+S")
        self.opcaoSalvarComo.setDisabled(True)

        self.menuArquivo.addSeparator()
        self.opcaoFechar = self.menuArquivo.addAction("F&echar")
        self.opcaoFechar.setShortcut("Ctrl+X")
        self.opcaoFechar.triggered.connect(self.close)

        self.gerarListasFiltros()

        self.opcaoSobre = self.menuSobre.addAction("S&obre o Aplicativo")
        self.opcaoSobre.triggered.connect(self.mostrarInformacoesSobre)
        self.opcaoInfoImagem = self.menuSobre.addAction("&Informacões da Imagem")
        self.opcaoInfoImagem.triggered.connect(self.mostrarInformacoesSobre)
        self.opcaoInfoImagem.setVisible(True)

        # Criar barra de status
        self.barraStatus = self.statusBar()
        self.barraStatus.showMessage("Seja bem-vindo ao meu aplicativo", 5000)

        # Criando a barra de progresso
        self.barraProgresso = QProgressBar()

        # Timer
        self.timer = QTimer()
        # self.timer.setInterval(1000)

        # Criando Labels
        self.barraProgressoTexto = QLabel("Progresso")

        # Criando imagens
        self.imagemOriginal = QLabel()
        self.endImagemOriginal = ''
        self.endImagemResultado = ''

    def gerarListasFiltros(self):

        self.criarActionCorrecaoGama()
        self.criarActionFiltroGaussiano()
        self.criarActionFiltroMediana()
        self.criarActionFiltroNegativo()
        self.criarActionTransformacaoLogaritmica()
        self.criarActionFiltroDeteccaoDeBordas()
        self.criarActionFiltroSharpen()
        self.criarActionFiltroSobel()
        self.criarActionExtrairCamadaRGB()
        self.criarActionConverterEscalaCinza()
        self.criarActionConverterPretoBranco()
        self.criarActionTransformacaoMorfologica()
      
       

        self.listaFiltrosColoridaCinza = [self.correcaoGama, self.filtroGaussiano, self.filtroMediana,
                                     self.filtroNegativo, self.transformacaoLogaritmica,
                                     self.filtroDeteccaoDeBordas, self.filtroSharpen, self.filtroSobel,
                                     self.extrairCamadaRGB, self.converterEscalaCinza, self.converterPretoBranco]

        self.listaFiltrosPretoBranco = [self.filtroDeteccaoDeBordas, self.transformacaoMorfologica]
    

    def criarActionCorrecaoGama(self):
        self.correcaoGama = self.menuTransformacao.addAction("Filtro Correção &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.setDisabled(True)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)
        self.correcaoGama.triggered.connect(lambda:
                                            self.transformarImagem(self.correcaoGama, 'CorrecaoGama',
                                                                   self.extensaoImagemOriginal))

    def criarActionFiltroGaussiano(self):
        self.filtroGaussiano = self.menuTransformacao.addAction("Filtro Ga&ussiano")
        self.filtroGaussiano.setShortcut("Ctrl+Shift+U")
        self.filtroGaussiano.setDisabled(True)
        self.filtroGaussiano.setCheckable(True)
        self.filtroGaussiano.setChecked(False)
        self.filtroGaussiano.triggered.connect(
            lambda: self.transformarImagem(self.filtroGaussiano, 'Gaussiano3x3', self.extensaoImagemOriginal))

    def criarActionFiltroMediana(self):

        self.filtroMediana = self.menuTransformacao.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.setDisabled(True)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)
        self.filtroMediana.triggered.connect(
            lambda: self.transformarImagem(self.filtroMediana, 'Mediana', self.extensaoImagemOriginal))

    def criarActionFiltroNegativo(self):
        self.filtroNegativo = self.menuTransformacao.addAction("Filtro &Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.setDisabled(True)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)
        self.filtroNegativo.triggered.connect(
            lambda: self.transformarImagem(self.filtroNegativo, 'Negativo', self.extensaoImagemOriginal))

    def criarActionTransformacaoLogaritmica(self):
        self.transformacaoLogaritmica = self.menuTransformacao.addAction("Transformação &Logarítmica")
        self.transformacaoLogaritmica.setShortcut("Ctrl+Shift+L")
        self.transformacaoLogaritmica.setDisabled(True)
        self.transformacaoLogaritmica.setCheckable(True)
        self.transformacaoLogaritmica.setChecked(False)
        self.transformacaoLogaritmica.triggered.connect(
            lambda: self.transformarImagem(self.transformacaoLogaritmica, 'TransformacaoLogaritmica',
                                   self.extensaoImagemOriginal))

    def criarActionFiltroDeteccaoDeBordas(self):
        self.filtroDeteccaoDeBordas = self.menuTransformacao.addAction("Filtros &Detecção de Bordas")
        self.filtroDeteccaoDeBordas.setShortcut("Ctrl+Shift+D")
        self.filtroDeteccaoDeBordas.setDisabled(True)
        self.filtroDeteccaoDeBordas.setCheckable(True)
        self.filtroDeteccaoDeBordas.setChecked(False)
        self.filtroDeteccaoDeBordas.triggered.connect(
            lambda: self.transformarImagem(self.filtroDeteccaoDeBordas, 'EdgeDetection', self.extensaoImagemOriginal))

    def criarActionFiltroSharpen(self):
        self.filtroSharpen = self.menuTransformacao.addAction("Filtro S&harpen")
        self.filtroSharpen.setShortcut("Ctrl+Shift+H")
        self.filtroSharpen.setDisabled(True)
        self.filtroSharpen.setCheckable(True)
        self.filtroSharpen.setChecked(False)
        self.filtroSharpen.triggered.connect(
            lambda: self.transformarImagem(self.filtroSharpen, 'Sharpen', self.extensaoImagemOriginal))

    def criarActionFiltroSobel(self):
        self.filtroSobel = self.menuTransformacao.addAction("Filtro S&obel")
        self.filtroSobel.setShortcut("Ctrl+Shift+O")
        self.filtroSobel.setDisabled(True)
        self.filtroSobel.setCheckable(True)
        self.filtroSobel.setChecked(False)
        self.filtroSobel.triggered.connect(
            lambda: self.transformarImagem(self.filtroSobel, 'Sobel', self.extensaoImagemOriginal))

    def criarActionExtrairCamadaRGB(self):
        self.extrairCamadaRGB = self.menuTransformacao.addAction("Extrair &Camadas RGB")
        self.extrairCamadaRGB.setShortcut("Ctrl+Shift+C")
        self.extrairCamadaRGB.setDisabled(True)
        self.extrairCamadaRGB.setCheckable(True)
        self.extrairCamadaRGB.setChecked(False)
        self.extrairCamadaRGB.triggered.connect(
            lambda: self.transformarImagem(self.extrairCamadaRGB, 'CamadaR', '.ppm'))

    def criarActionConverterEscalaCinza(self):
        self.converterEscalaCinza = self.menuTransformacao.addAction("Converter para Escala de C&inza")
        self.converterEscalaCinza.setShortcut("Ctrl+Shift+I")
        self.converterEscalaCinza.setDisabled(True)
        self.converterEscalaCinza.setCheckable(True)
        self.converterEscalaCinza.setChecked(False)
        self.converterEscalaCinza.triggered.connect(
            lambda: self.transformarImagem(self.converterEscalaCinza, 'ConverterEscalaDeCinza', '.pgm'))

    def criarActionConverterPretoBranco(self):
        self.converterPretoBranco = self.menuTransformacao.addAction("Converter Pre&to e Branco")
        self.converterPretoBranco.setShortcut("Ctrl+Shift+T")
        self.converterPretoBranco.setDisabled(True)
        self.converterPretoBranco.setCheckable(True)
        self.converterPretoBranco.setChecked(False)
        self.converterPretoBranco.triggered.connect(
            lambda: self.transformarImagem(self.converterPretoBranco, 'Binaria', '.pbm'))

    def criarActionTransformacaoMorfologica(self):
        self.transformacaoMorfologica = self.menuTransformacao.addAction("&Morfológicas")
        self.transformacaoMorfologica.setShortcut("Ctrl+Shift+M")
        self.transformacaoMorfologica.setDisabled(True)
        self.transformacaoMorfologica.setCheckable(True)
        self.transformacaoMorfologica.setChecked(False)
        self.transformacaoMorfologica.triggered.connect(
            lambda: self.transformarImagem(self.transformacaoMorfologica, 'Erosao', '.pbm'))



    def gerarLayouts(self):
        # Criando janela
        self.janelaAreaVisualizacao = QWidget(self)
        self.setCentralWidget(self.janelaAreaVisualizacao)

        # Criando os layouts
        self.layoutPrincipal = QVBoxLayout()
        self.layoutTopo = QVBoxLayout()
        self.layoutRodape = QHBoxLayout()

        # Adicionando os widgets
        self.layoutTopo.addWidget(self.imagemOriginal)
        self.layoutRodape.addWidget(self.barraProgressoTexto)
        self.layoutRodape.addWidget(self.barraProgresso)

        # Adicionando layouts filhos na janela principal
        self.layoutPrincipal.addLayout(self.layoutTopo, 80)
        self.layoutPrincipal.addLayout(self.layoutRodape, 20)

        self.janelaAreaVisualizacao.setLayout(self.layoutPrincipal)

    "Exibe informações sobre aplicativo e imagem quando selecionado menu Sobre"
    def mostrarInformacoesSobre(self):

        self.opcaoEscolhida = self.sender().text()
        self.caixaMensagem = QMessageBox()
      
        self.caixaMensagem.setIcon(QMessageBox.Information)

        if self.opcaoEscolhida == "S&obre o Aplicativo":
            self.caixaMensagem.setWindowIcon(QIcon("imagens/youpi.png"))
            self.caixaMensagem.setWindowTitle("Sobre o Aplicativo")
            self.caixaMensagem.setText("Desenvolvido por Hudson Salis Evangelista\n\nEste aplicativo tem como princípio a realização de  transformações em imagens com extensão pgm, ppm e pbm e foi elaborado para o trabalho final da disciplina de Processamento Digital de Imagens no Curso Superior em Análise e Desenvolvimento de Sistemas do Instituto Federal de Educação, Ciência e Tecnologia do Triângulo Mineiro - IFTM "
            "\nItuiutaba-MG \n\nTrabalho terminado em 07 de Agosto de 2020")
            self.caixaMensagem.setInformativeText('<a href="https://www.youtube.com/watch?v=xlUkxHyXOCA">Link do vídeo no Youtube</a>')
           
            self.caixaMensagem.exec_()

        if self.opcaoEscolhida == "&Informacões da Imagem":
            if self.endImagemOriginal != '':
                self.caixaMensagem.setWindowTitle("Informações da Imagem")

                self.extrairInfoImagem()

                self.caixaMensagem.setText("Arquivo: " + self.nomeimagem + "\n" + "Tipo: " + self.tipoimagem +
                                           "Comentário: " + self.comentarioimagem + "Largura: " + self.larguraimagem \
                                           + "\n" + "Altura: " + self.alturaimagem)

                self.caixaMensagem.exec_()

    	#4682B4
   

    "Salva uma cópia da imagem com o nome do arquivo e diretório escolhidos pelo usuário depois de verificar se existe uma imagem"
    def salvarImagemComo(self):
        global extensaoImagemResultado
        try:
            if self.endImagemOriginal != '':
                imagemSalvaComo, tipos = QFileDialog.getSaveFileName(self, caption='Salvar como',
                                                                     directory=QtCore.QDir.currentPath(),
                                                                     filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                                     initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')
                if imagemSalvaComo:
                    self.parts = imagemSalvaComo.rpartition('/')
                    self.endereco = self.parts[0]
                    if self.endImagemResultado != '':
                        shutil.copyfile(self.endImagemResultado, self.endereco + '/' +
                                        os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                        extensaoImagemResultado)
                    else:
                        shutil.copyfile(self.endImagemOriginal, self.endereco + '/' +
                                        os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                        self.extensaoImagemOriginal)
        except:
            pass

   

    def abrirImagem(self):
        global imagemResultado

        self.ocultarDiretorioImgResultado()

        global porcentagemProgresso
        arquivoImagem, _ = QFileDialog.getOpenFileName(self, caption="Abrir Imagem",
                                                       directory=QtCore.QDir.currentPath(),
                                                       filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                       initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')

        if arquivoImagem:
            self.excluirCopiaImgTransformada()
            self.removerChecagemFiltrosUsados()
            porcentagemProgresso = 0
            self.barraProgresso.setValue(porcentagemProgresso)
            self.endImagemOriginal = arquivoImagem
            self.pixmapImagem = QPixmap(self.endImagemOriginal)
            self.extensaoImagemOriginal = os.path.splitext(os.path.basename(arquivoImagem))[1]
            self.exibirImagem()
            self.alterarVisibilidadeMenus()

    def extrairInfoImagem(self):
        try:
            self.parts = self.endImagemOriginal.rpartition('/')
            self.nomeimagem = self.parts[2]
            self.leituraimagem = open(self.endImagemOriginal, "r+")
            self.tipoimagem = self.leituraimagem.readline()
            self.comentarioimagem = self.leituraimagem.readline()
            self.dimensoesimagem = self.leituraimagem.readline()
            self.dimensoesimagem = self.dimensoesimagem.split()
            self.larguraimagem = self.dimensoesimagem[0]
            self.alturaimagem = self.dimensoesimagem[1]
        except:
            pass

    "Realiza a aplicação de filtros e transformações nas imagens, apresentando o na barra de progresso e de status" 
    def transformarImagem(self, filtro, script, extensao):

        global porcentagemProgresso
        global imagemResultado
        global extensaoImagemResultado
        global listaFiltrosUsados

        porcentagemProgresso = 0
        self.barraProgresso.setValue(porcentagemProgresso)
        self.filtroUsado = ''

        if os.path.exists(imagemResultado + "Copia" + extensaoImagemResultado):
            self.argumentoEntrada = imagemResultado + "Copia" + extensaoImagemResultado
        else:
            self.argumentoEntrada = self.endImagemOriginal

        try:
            if self.extensaoImagemOriginal == '.ppm':
                self.script = 'filtrosDeTransformacao/colorida/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            elif self.extensaoImagemOriginal == '.pgm':
                self.script = 'filtrosDeTransformacao/escalaCinza/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            elif self.extensaoImagemOriginal == '.pbm':
                self.script = 'filtrosDeTransformacao/pretoBranco/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            self.argumentos = 'python ' + self.script + ' \"' + self.argumentoEntrada + '\" ' + \
                              imagemResultado + extensaoImagemResultado
            self.executarTransformacao = subprocess.run(self.argumentos, shell=True)

            while porcentagemProgresso < 100:
                if self.executarTransformacao is not None:
                    porcentagemProgresso += 0.001
                    self.barraProgresso.setValue(int(porcentagemProgresso))
                else:
                    break

            self.endImagemResultado = imagemResultado + extensaoImagemResultado
            self.pixmapImagem = QPixmap(self.endImagemResultado)
            shutil.copyfile(self.endImagemResultado, imagemResultado + "Copia" + extensaoImagemResultado)
            self.exibirImagem()
            listaFiltrosUsados.append(self.filtroUsado)
            self.extensaoImagemOriginal = extensaoImagemResultado
            self.alterarVisibilidadeMenus()

            self.barraStatus.showMessage("Aplicação " + self.filtroEscolhido.replace("&", "") +
                                         " finalizada", 5000)
        except:
            pass

    def exibirImagem(self):
        if self.pixmapImagem.width() > int(GetSystemMetrics(0) / 2) or \
                self.pixmapImagem.height() > int(GetSystemMetrics(1) / 2):
            self.pixmapImagem = self.pixmapImagem.scaled(int(GetSystemMetrics(0) / 2), int(GetSystemMetrics(1) / 2),
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.imagemOriginal.setPixmap(self.pixmapImagem)
        self.imagemOriginal.setAlignment(QtCore.Qt.AlignCenter)

    def excluirCopiaImgTransformada(self):
        global imagemResultado
        try:
            if os.path.exists(imagemResultado + "Copia" + '.ppm') or os.path.exists(imagemResultado + '.ppm'):
                os.remove(imagemResultado + "Copia" + '.ppm')
                os.remove(imagemResultado + '.ppm')

            if os.path.exists(imagemResultado + "Copia" + '.pgm') or os.path.exists(imagemResultado + '.pgm'):
                os.remove(imagemResultado + "Copia" + '.pgm')
                os.remove(imagemResultado + '.pgm')

            if os.path.exists(imagemResultado + "Copia" + '.pbm') or os.path.exists(imagemResultado + '.pbm'):
                os.remove(imagemResultado + "Copia" + '.pbm')
                os.remove(imagemResultado + '.pbm')
        except:
            pass

    def alterarVisibilidadeMenus(self):

        self.opcaoInfoImagem.setVisible(True)
        self.opcaoSalvarComo.setDisabled(False)

        if self.extensaoImagemOriginal == '.ppm':
            for filtro in self.listaFiltrosColoridaCinza:
                filtro.setDisabled(False)
            self.transformacaoMorfologica.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pgm':
            for filtro in self.listaFiltrosColoridaCinza:
                    filtro.setDisabled(False)
            self.extrairCamadaRGB.setDisabled(True)
            self.converterEscalaCinza.setDisabled(True)
            self.transformacaoMorfologica.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pbm':
            for filtro in self.listaFiltrosColoridaCinza:
                    filtro.setDisabled(True)

            self.filtroDeteccaoDeBordas.setDisabled(False)
            self.transformacaoMorfologica.setDisabled(False)

    def removerChecagemFiltrosUsados(self):
        global listaFiltrosUsados
        for filtro in listaFiltrosUsados:
            filtro.setChecked(False)

        listaFiltrosUsados.clear()

    def ocultarDiretorioImgResultado(self):
        os.system("attrib +h " + 'imagensResultado')

    "Excluir imagens cópias quando fechar o aplicativo para evitar futuros erros"
    def closeEvent(self, event):
        global listaFiltrosUsados
        self.excluirCopiaImgTransformada()


    def link(self, linkStr):

        QDesktopServices.openUrl(QUrl(linkStr))

        
    

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

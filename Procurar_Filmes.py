import sys
import requests
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListView, QGraphicsView, QLineEdit, QPushButton, QRadioButton, QStatusBar, QListWidgetItem,
from PyQt6.QtGui import QStandardItem, QFont
from requests.exceptions import HTTPError

from apiResult import ApiResult
from movie import Movie


class FormFilmes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.filmes_pesquisa = []
        self.filmes_dict = {}
        self.api_key = "041d54f461d20ffccc78361f1c121792"
        self.api_base_url = "https://api.themoviedb.org/3"
        self.api_url = f"{self.api_base_url}/discover/movie"
        self.ltv_Filmes = QListView()
        self.filmes_dict = {}
        self.rbt_Comedia = QRadioButton("Comedia")
        self.rbt_Acao = QRadioButton("Acao")
        self.rbt_Aventura = QRadioButton("Aventura")

        # Conectar os sinais dos radio buttons à função rbt_Categoria_CheckedChanged
        self.rbt_Comedia.toggled.connect(self.rbt_Categoria_CheckedChanged)
        self.rbt_Acao.toggled.connect(self.rbt_Categoria_CheckedChanged)
        self.rbt_Aventura.toggled.connect(self.rbt_Categoria_CheckedChanged)

    def setupUi(self, Procurar_Filme):
        Procurar_Filme.setObjectName("Procurar_Filme")
        Procurar_Filme.resize(505, 447)
        Procurar_Filme.setStyleSheet("background-color: rgb(0, 170, 255);")
        Procurar_Filme.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QWidget(parent=Procurar_Filme)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.ltv_Filmes = QListView(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.ltv_Filmes.setFont(font)
        self.ltv_Filmes.setStyleSheet("background-color: rgb(203, 203, 203);")
        self.ltv_Filmes.setObjectName("ltv_Filmes")
        self.verticalLayout.addWidget(self.ltv_Filmes)

        self.gp_Fotofilme = QGraphicsView(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.gp_Fotofilme.setFont(font)
        self.gp_Fotofilme.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.gp_Fotofilme.setObjectName("gp_Fotofilme")
        self.verticalLayout.addWidget(self.gp_Fotofilme)

        self.ln_Pesquisar = QLineEdit(parent=self.centralwidget)
        self.ln_Pesquisar.setStyleSheet(
            "background-color: rgb(197, 197, 197);")
        self.ln_Pesquisar.setObjectName("ln_Pesquisar")
        self.verticalLayout.addWidget(self.ln_Pesquisar)

        self.btn_Pesquisar = QPushButton(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.btn_Pesquisar.setFont(font)
        self.btn_Pesquisar.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_Pesquisar.setObjectName("btn_Pesquisar")
        self.verticalLayout.addWidget(self.btn_Pesquisar)

        self.rbt_Comedia = QRadioButton(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.rbt_Comedia.setFont(font)
        self.rbt_Comedia.setObjectName("rbt_Comedia")
        self.verticalLayout.addWidget(self.rbt_Comedia)

        self.rbt_Acao = QRadioButton(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.rbt_Acao.setFont(font)
        self.rbt_Acao.setStyleSheet("border-top-color: rgb(255, 0, 0);")
        self.rbt_Acao.setObjectName("rbt_Acao")
        self.verticalLayout.addWidget(self.rbt_Acao)

        self.rbt_Aventura = QRadioButton(parent=self.centralwidget)
        font = QFont()
        font.setBold(True)
        self.rbt_Aventura.setFont(font)
        self.rbt_Aventura.setObjectName("rbt_Aventura")
        self.verticalLayout.addWidget(self.rbt_Aventura)

        Procurar_Filme.setCentralWidget(self.centralwidget)
        self.sttb_Filmes = QStatusBar(parent=Procurar_Filme)
        self.sttb_Filmes.setObjectName("sttb_Filmes")
        Procurar_Filme.setStatusBar(self.sttb_Filmes)

        self.retranslateUi(Procurar_Filme)
        QtCore.QMetaObject.connectSlotsByName(Procurar_Filme)

        self.btn_Pesquisar.clicked.connect(self.btn_Pesquisar_Click)
        self.rbt_Comedia.clicked.connect(self.rbt_Categoria_CheckedChanged)
        self.rbt_Acao.clicked.connect(self.rbt_Categoria_CheckedChanged)
        self.rbt_Aventura.clicked.connect(self.rbt_Categoria_CheckedChanged)

    def retranslateUi(self, Procurar_Filme):
        _translate = QtCore.QCoreApplication.translate
        Procurar_Filme.setWindowTitle(_translate(
            "Procurar_Filme", "Procurar Filmes"))
        self.btn_Pesquisar.setText(_translate("Procurar_Filme", "Pesquisar"))
        self.rbt_Comedia.setText(_translate("Procurar_Filme", "Comedia"))
        self.rbt_Acao.setText(_translate("Procurar_Filme", "Acao"))
        self.rbt_Aventura.setText(_translate("Procurar_Filme", "Aventura"))

    def ObterMelhoresFilmesCategoria(self, genreId):
        params = {
            "api_key": self.api_key,
            "with_genres": str(genreId),
            "sort_by": "popularity.desc",
            "total_pages": "5",
            "language": "pt-BR",
        }

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            json_data = response.json()

            # Aqui você pode processar os resultados da API
            results = json_data.get("results", [])
            for movie in results:
                title = movie.get("title", "")
                release_date = movie.get("release_date", "")
                print(f"Title: {title}, Release Date: {release_date}")

        except requests.exceptions.RequestException as e:
            return f"Error making request: {e}"

    def rbt_Categoria_CheckedChanged(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            # Extrai o sufixo do nome do radio button (por exemplo, "Comedia")
            categoria_nome = radio_button.text()

            # Mapeia o nome da categoria para um ID (ou use uma lógica mais avançada se necessário)
            genreid = self.ObterGenreIdPorNome(categoria_nome)

            # Chama a API com o ID da categoria
            self.ObterMelhoresFilmesCategoria(genreid)

    def ObterGenreIdPorNome(self, categoria_nome):
        # Ajuste a lógica de mapeamento conforme necessário
        # Converte para minúsculas para evitar problemas de case
        categoria_nome = categoria_nome.lower()
        if categoria_nome == "comedia":
            return 35  # ID da categoria de comédia (exemplo)
        elif categoria_nome == "acao":
            return 28  # ID da categoria de ação (exemplo)
        elif categoria_nome == "aventura":
            return 12  # ID da categoria de aventura (exemplo)
        else:
            raise ValueError(f"Categoria nao reconhecida: {categoria_nome}")

    def btn_Pesquisar_Click(self):
        nome_filme = self.ln_Pesquisar.text()

        # Adicione um print para verificar o conteúdo de nome_filme
        print("Nome do filme:", nome_filme)

        self.filmes_pesquisa = self.PesquisarFilme(nome_filme)

        # Adicione um print para verificar o conteúdo de filmes_pesquisa
        print("Filmes Pesquisa:", self.filmes_pesquisa)

        # Chame a função ExibirResultados
        self.ExibirResultados(self.filmes_pesquisa)

        # Adicione um print para verificar se a função foi chamada
        print("ExibirResultados chamada")

    def PesquisarFilme(self, nome_filme):
        endpoint = f"{self.api_base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": nome_filme,
            "language": "pt-BR",
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            json_data = response.json()
            resultado = ApiResult(results=json_data.get("results", []))

            # Adiciona o ID ao resultado
            filmes_com_id = [
                Movie(
                    id=filme["id"],
                    title=filme["title"],
                    overview=filme["overview"],
                    # Verifica se 'cast' está presente
                    cast=filme.get("cast", []),
                    release_date=filme["release_date"],
                    vote_average=filme["vote_average"],
                    poster_path=filme["poster_path"],
                )
                for filme in resultado.results
            ]

            return filmes_com_id

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            print(f"An error occurred: {err}")
            raise

    def ExibirResultados(self, filmes):
        # Verifica se o modelo já existe
        if not hasattr(self, 'model'):
            # Se não existir, cria um novo modelo
            self.model = QtGui.QStandardItemModel()
            self.ltv_Filmes.setModel(self.model)

            # Limpa o modelo antes de adicionar novos itens
            self.model.clear()

            for filme in filmes:
                # Cria um novo item QStandardItem para cada filme
                item = QStandardItem(
                    f"{filme.title} ({filme.release_date})")

                # Armazena o objeto do filme na propriedade data para fácil acesso
                item.setData(filme, Qt.ItemDataRole.UserRole)

                # Adiciona o item ao modelo
                self.model.appendRow(item)

                # Adiciona o filme ao dicionário (se necessário)
                self.filmes_dict[filme.id] = filme

    def ltv_Filmes_DoubleClick(self, index):
        if index.isValid():
            selected_item = self.ltv_Filmes.itemFromIndex(index)
            selected_movie = selected_item.data(Qt.ItemDataRole.UserRole)

            # Verifica se selected_movie é nulo antes de tentar acessar suas propriedades
            if selected_movie:
                # Exibe os detalhes quando um item é clicado duas vezes
                self.ExibirDetalhes(selected_movie)

    def ExibirDetalhes(self, filme):
        self.ltv_Filmes.clear()

        if filme:
            # Cria um novo item ListViewItem para cada detalhe
            self.ltv_Filmes.addItem(
                QListWidgetItem(f"Titulo: {filme.title}"))
            self.ltv_Filmes.addItem(
                QListWidgetItem(f"Sinopse: {filme.overview}"))

            # Verifica se a lista de atores não é nula antes de acessar seus elementos
            if filme.cast:
                self.ltv_Filmes.addItem(QListWidgetItem(
                    f"Atores: {', '.join(filme.cast)}"))
            else:
                self.ltv_Filmes.addItem(QListWidgetItem(
                    "Atores: Informação não disponível"))

            self.ltv_Filmes.addItem(QListWidgetItem(
                f"Ano de lançamento: {filme.release_date}"))
            self.ltv_Filmes.addItem(QListWidgetItem(
                f"Nota: {filme.vote_average}"))

        else:
            self.ltv_Filmes.addItem(
                QListWidgetItem("Filme não encontrado."))

    def closeEvent(self, event):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Procurar_Filme = FormFilmes()
    Procurar_Filme.show()
    sys.exit(app.exec())

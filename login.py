# ok 1. Crie uma aplicação do zero seguindo a documentação (https://flask.palletsprojects.com/en/stable/); ok
# ok 2. Anotem comandos que vocês sabem ou acham que vão se repetir e que vão precisar no futuro durante o desenvolvimento (para facilitar nossa vida); ok
# ok 3. Criar uma página index para boas-vindas e formulário de login (se o usuário estiver logado, podemos redirecionar para a página do usuário);
# 4. O processo de autenticação deverá ser feito com dados temporário dentro do código da aplicação. Por exemplo, crie uma lista fictícia de usuários e senhas para validação. Se a autenticação der certo, redirecionar para a página inicial do usuário. Se deu errado, volta para o login e mostra alguma mensagem de erro.
# 5. Com o usuário logado, na página do usuário, quero poder adicionar, remover, buscar, editar e listas suas músicas preferidas;
# 6. Criar uma página específica para manipular as músicas; e
# 7. Sair da sessão (logout).

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ListaUsuarios = [
    {'usuario': 'admin', 'senha': 'admin123'},
    {'usuario': 'user1', 'senha': 'senha1'},
    {'usuario': 'user2', 'senha': 'senha2'}
]


class Musica:
    def __init__(self, titulo, artista):
        self.titulo = titulo
        self.artista = artista
    def tostring(self):
        return f"{self.titulo} - {self.artista}"

class Playlist:
    musicas=[]
    def adicionarMusica(self, Musica):
        self.musicas.append(Musica)
    def removerMusica(self, Musica):
        if Musica in self.musicas:
            self.musicas.remove(Musica.index(Musica))
        else:
            print("Música não encontrada na playlist.")
    def editarMusica(self, MusicaAntiga, MusicaNova):
        if MusicaAntiga in self.musicas:
            index = self.musicas.index(MusicaAntiga)
            self.musicas[index] = MusicaNova
        else:
            print("Música não encontrada na playlist.")

m1 = Musica("Blinding Lights", "The Weeknd")
m2 = Musica("Shape of You", "Ed Sheeran")

m = Playlist()
m.adicionarMusica(m1.tostring())
m.adicionarMusica(m2.tostring())
print(m.musicas)

@app.route("/")
def index():
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if validar_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Usuário ou senha inválidos. Tente novamente.'
            print(error)
    return render_template('login.html', error=error)

def validar_login(username, password):
    for user in ListaUsuarios:
        if user['usuario'] == username and user['senha'] == password:
            return True
    return False


def log_the_user_in(username):
    return render_template('index.html', username=username, playlist=m.musicas)


@app.route('/adicionar', methods=['POST'])
def adicionarMusica():
    erro = None
    titulo = request.form.get('titulo', '').strip()
    artista = request.form.get('artista', '').strip()

    if titulo == "" or artista == "":
        erro = 'Título ou artista não podem ser vazios.'
    else:
        m3 = Musica(titulo, artista)
        m.adicionarMusica(m3.tostring())

    return render_template('index.html', error=erro, playlist=m.musicas)

@app.route('/remover', methods=['POST'])
def removerMusica():
    erro = None
    titulo = request.form.get('titulo', '').strip()
    artista = request.form.get('artista', '').strip()

    if titulo == "" or artista == "":
        erro = 'Título ou artista não podem ser vazios.'
    else:
        m3 = Musica(titulo, artista)
        m.removerMusica(m3.tostring())

    return render_template('index.html', error=erro, playlist=m.musicas)



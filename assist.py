import speech_recognition as sr  #Reconhecimento de voz
import pyttsx3  #Conversão de texto em fala
import datetime  #Obtenção e manipulação da data e hora
import wikipedia  #Pesquisas na Wikipedia
import pywhatkit  #Toca músicas redirecionando pro YouTube
import os  #Interação com o sistema operacional
import spotipy  #API de controle e acesso ao Spotify
from spotipy.oauth2 import SpotifyOAuth  # Autenticação no Spotify
import time  #Manipulação de tempo 
from horas_util import depuraHora  #Função para formatar e anunciar as horas corretamente
import webbrowser  #Abre URLs e faz pesquisas no navegador
import pvporcupine  #API de detecção de palavras-chave (wake word)
import pyaudio #Manipulação de áudio em tempo real
import struct #Manipulação de dados binários (conversão de áudio, por exemplo)
import re #Expressões regulares (manipulação e busca em strings)

audio = sr.Recognizer() #Cria uma instância do Recognizer, que permite capturar e processar o áudio.
audio.pause_threshold = 1.5 #Ajuste do threshold de pausa para 3 segundos  
maquina = pyttsx3.init() #Inicializa o mecanismo de conversão de texto em fala (pyttsx3), configurando a "máquina" que vai falar.

#Função que utiliza da API do porcupine pra reconhecer se foi dita a palavra "Joana"
def picovoice():
    ACCESS_KEY = "Oct7nsM7nTjtsdE0uv40+TS+yn2KXZp8HycU0OHi2YSAMQJAokq5PQ==" # Chave do porcupine

    # Inicializa o Porcupine com uma palavra-chave padrão 
    handle = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=["C:\\Users\\Oem\\OneDrive\\Documentos\\Git-Hub\\joanAdarV\\joana.ppn"], #Caminho para seu documento .ppn disponibilizado pelo picovoice para reconhecimento de palavra-chave
        model_path="C:\\Users\\Oem\\OneDrive\\Documentos\\Git-Hub\\joanAdarV\\porcupine_params_pt.pv", #Caminho para seu documento .ppn que contém os parâmetros de reconhecimento para o idioma português
        sensitivities=[1]
    )

    # Configura o PyAudio para captura de áudio
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=handle.sample_rate,
        input=True,
        frames_per_buffer=handle.frame_length
    )

    print("Aguardando palavra-chave...")

    try:
        while True:
            # Lê dados de áudio do microfone
            pcm = stream.read(handle.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * handle.frame_length, pcm)

            # Processa o áudio e verifica a palavra-chave
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                print("Palavra-chave detectada!")
                return True
    except KeyboardInterrupt:
        print("Finalizando...")
    finally:
        # Fecha os recursos
        stream.close()
        p.terminate()
        handle.delete()

# Configuração do Spotipy com suas credenciais
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="e023400eddca4653ae81308d57de046c", #Seu client_id forncido pelo Spotify for Developers
    client_secret="311d2b782aa548329da6f0feddeeff6e",#Seu client_secret, também fornecido pelo Spotify for Developers
    redirect_uri="http://localhost:8888/callback",# URL de redirecionamento(Precisa ser a mesma na API do Spotify for Developers)
    scope="user-modify-playback-state user-read-playback-state"
))

#Abre o Spotify
def abrir_spotify():
    """Abre o aplicativo Spotify no computador."""
    try:
        os.startfile("spotify")  # Para Windows, o comando é esse
        # os.system("open -a Spotify") ou subprocess.run(["spotify"])
        # Atraso para garantir que o Spotify esteja carregado
        time.sleep(5)  # Aguarda 5 segundos 
    except Exception as e:
        print(f"Erro ao abrir o Spotify: {e}")

#Obtém o URI da playlist pedida no comando
def obter_uri_playlist(nome_playlist):
    try:
        # Busca as playlists do usuário
        playlists = sp.current_user_playlists(limit=50)  # Faz a pesquisa de playlists e impõe um limite máximo de playlists retornadas
        for playlist in playlists['items']:
            if playlist is None: #Se aparecer algum item 'None' o código vai ignorar e seguir 
                continue
            if playlist['name'].lower() == nome_playlist:#Verifica se o nome bate
                uri = playlist.get('uri', None)
                return uri#Retorna o URI da playlist
        print("Essa playlist {nome_playlist} não foi encontrada.") 
        maquina.say("Playlist não encontrada.")
        maquina.runAndWait()
        return None
    except Exception as e:
        print(f"Erro ao buscar playlists: {e}")
        maquina.say("Erro ao buscar playlists.")
        maquina.runAndWait()
        return None
#Obtém o URI da música pedida no comando
def obter_uri_musica(nome_musica):
    try:
        resultado = sp.search(q=nome_musica, type='track', limit=10)#Procura a música
        if resultado['tracks']['items']:
            return resultado['tracks']['items'][0]['uri']#Retorna o URI da música
        else:
            print("Essa música {nome_musica} não foi encontrada.")
            maquina.say("Música não encontrada.")
            maquina.runAndWait()
            return None
    except Exception as e:
        print("Erro ao buscar música: {e}")
        maquina.say("Erro ao buscar música.")
        maquina.runAndWait()
        return None

#Verifica se a música pedida no comando realmente existe na playlist
def verificarMusicaPlaylist(uri_playlist, uri_musica, nome_musica):
    try:
        faixas = sp.playlist_tracks(uri_playlist)  # Pega as faixas da playlist
        if 'items' not in faixas or not faixas['items']:  # Verifica se 'items' está presente e não é nulo
            print("A playlist não contém músicas ou ocorreu um erro ao obter as faixas.")
            maquina.say("A playlist não contém músicas ou ocorreu um erro ao obter as faixas")
            maquina.runAndWait()
            return False

        for faixa in faixas['items']:
            if faixa is None or 'track' not in faixa or not faixa['track']:  # Ignorar faixas inválidas (None ou com campos ausentes)
                continue
            uri_faixa = faixa['track'].get('uri', '')
            if uri_musica in uri_faixa:
                print(f"A música '{nome_musica}' está na playlist.")
                return True
        print(f"A música '{nome_musica}' não está na playlist.")
        maquina.say("Essa música não está na playlist.")
        maquina.runAndWait()
        return False

    except Exception as e:
        print(f"Erro ao buscar faixas da playlist: {e}")
        maquina.say("Erro ao buscar faixas da playlist")
        maquina.runAndWait()
        return False

#Toca alguma música dentro de uma playlist
def tocarMusicaPlaylist(uri_playlist, uri_musica, device_id):
    try:       
        #Recuperar TODAS as faixas da playlist (incluindo paginação)
        tracks = []
        playlist = sp.playlist_tracks(uri_playlist)
        while playlist:
            tracks.extend(playlist.get('items', []))
            playlist = sp.next(playlist) if playlist.get('next') else None

        #Filtrar itens válidos (remover None ou itens sem chave 'track' ou 'uri')
        valid_tracks = [
            track for track in tracks
            if track is not None and 'track' in track and track['track'] and 'uri' in track['track']
        ]

        #Encontrar a posição (offset) da música desejada na playlist
        offset = next((index for index, track in enumerate(valid_tracks) if track['track']['uri'] == uri_musica), None)
        '''
        #Adiciona mais um número no offset quando alguma playlist retornar o número errado
        if uri_playlist == 'spotify:playlist:6tpOenAVIRyuUWfl2KRqri':
            offset = offset +1
        '''
        #Iniciar a reprodução da playlist a partir da música desejada no dispositivo especificado
        sp.start_playback(device_id=device_id, context_uri=uri_playlist, offset={"position": offset})

        print(f"Tocando a música {uri_musica} da playlist {uri_playlist} no dispositivo {device_id} e continuando com as próximas.")
        return True
    except Exception as e:
        print(f"Erro ao tentar tocar a música: {e}")
        maquina.say("Houve algum erro ao tentar tocar a música")
        maquina.runAndWait()
        return False

# Identifica os dispositivos disponíveis
def dispositivos_conectados():
    try: 
        dispositivos = sp.devices()
        if dispositivos['devices']:
            return dispositivos['devices'][0]['id']
        else:
            print(f"Não há nenhum dispositivo conectado no momento")
            maquina.say("Não há nenhum dispositivo conectado no momento")
            maquina.runAndWait()
            return None
    except ConnectionError as e:
        print(f"Erro específico em dispositivos_conectados: {e}")
        maquina.say("Erro específico em dispositivos_conectados")
        maquina.runAndWait()
    except Exception as e:
        print(f"Erro genérico em dispositivos_conectados: {e}")
        maquina.say("Erro genérico em dispositivos_conectados")
        maquina.runAndWait()
    finally:
        print("Finalizando a verificação dos dispositivos.")
        
#Função pra descobrir o nome de uma playlist 
def descobreNome(palavraChave, frase):
    try: 
        palavras = frase.split()#Divide o texto em uma lista de palavras
        indice_chave = palavras.index(palavraChave)#Encontra o índice da palavra-chave
        if indice_chave + 1 < len(palavras):#Verifica se há uma palavra depois da chave
            nome_desejado = palavras[indice_chave + 1].lower()
            print(f"A sua palavra é: {nome_desejado}")
            return nome_desejado
        else: 
            print(f"Repita o nome da playlist ou da música novamente")
            maquina.say("Repita o nome da playlist ou da música novamente")
            maquina.runAndWait()
            return None
    except Exception as e:
        print(f"Erro na execução da função 'descobreNome': {e}")
        maquina.say("Erro na execução da função")
        maquina.runAndWait()

#Função pra descobrir o nome de uma música
def descobrePalavras(palavraChave, frase):
    try:
        # Divide a frase na palavra-chave e pega a parte que vem depois
        if palavraChave in frase:
            palavra_desejada = frase.split(palavraChave, 1)[1].strip()
            print(f"A sua palavra é: {palavra_desejada}")
            return palavra_desejada
        else:
            print(f"A palavra '{palavraChave}' não foi encontrada na frase.")
    except Exception as e:
        print(f"Erro na execução da função 'descobrePalavras': {e}")
        maquina.say("Erro na execução da função")
        maquina.runAndWait()

#Função que extrai o comando pedido 
def executa_comando():
    try:
        #O bloco 'with' garante que o microfone seja liberado corretamente após o uso
        with sr.Microphone() as source: #Usa o microfone como fonte de áudio e o nomeio de 'source'
            print("OUVINDO...")
            maquina.say("Ouvindo...")
            maquina.runAndWait()
            audio.adjust_for_ambient_noise(source, duration=1) # Ajuste automático da sensibilidade ao ruído de fundo
            voz = audio.listen(source) #Escuta o áudio do microfone e o armazena na variável voz
            comando = audio.recognize_google(voz, language='pt-Br') #Envia o áudio para o serviço de reconhecimento do Google, convertendo-o em texto e salvando-o na variável comando. Está configurado para processar áudio em português (pt-BR).
            comando = comando.lower() #Converte o texto para letras minúsculas para facilitar comparações.
    except sr.UnknownValueError: 
        print('Microfone não está ok')
        maquina.say("O microfone está com problemas")
        maquina.runAndWait()
    except sr.RequestError as e:
        print(f"Erro ao conectar ao serviço de reconhecimento de fala: {e}")
        maquina.say("Erro ao conectar ao serviço de reconhecimento de fala")
        maquina.runAndWait()
    return(comando)

#Função principal que executa o que comando de voz pediu
def comando_voz_usuario():
    try: 
        comando = executa_comando() #Ouve e processa o comando do usuário, armazenando o texto na variável comando.
        print("-="*30)
        print("Comando pedido:",comando)
        #"""
        if re.search(r"\b(hora|horário|horas)\b", comando): # Verifica se o comando contém a palavra "horas". Se sim, executa o bloco de código.
            hora = datetime.datetime.now().strftime('%H:%M') #Obtém a hora atual e formata
            horas = depuraHora(hora)
            print(horas)
            maquina.say('Agora são' + horas) #Faz a máquina "dizer" a hora atual.
            maquina.runAndWait() #Executa o comando de fala para a máquina dizer a hora.
        elif re.search(r"\b(me fale sobre)\b", comando): #Executa o comando para que a AV faça uma pesquisa na wikipedia e fale sobre oque ela achou
            procurar = comando.replace('me fale sobre', '')
            wikipedia.set_lang('pt')
            resultado = wikipedia.summary(procurar, 2)
            print(resultado)
            maquina.say(resultado)
            maquina.runAndWait()
        elif re.search(r"\b(pesquise por)\b", comando): # Faz a AV fazer alguma pesquisa no google 
            pesquisa = comando.replace('pesquise por', '')
            url = f"https://www.google.com/search?q={pesquisa}"
            webbrowser.open(url)
            print(f"Pesquisando por {pesquisa}")
            maquina.say(f"Pesquisando no google")
            maquina.runAndWait()
        elif re.search(r"\b(toque)\b", comando):
            musica = comando.replace('toque', '')
            #Reproduz a playlist desejada e uma música nessa playlist
            if 'playlist' in musica and 'música' in musica:
                palavra_chave1 = 'playlist'
                palavra_chave2 = 'música' 
                nome_playlist = descobreNome(palavra_chave1, musica) 
                nome_musica = descobrePalavras(palavra_chave2, musica)
                uri_playlist = obter_uri_playlist(nome_playlist)
                uri_musica = obter_uri_musica(nome_musica)
                print(f"A playlist é: {nome_playlist} com uri: {uri_playlist}\nA música é: {nome_musica}, com uri: {uri_musica} ")
                if uri_musica and uri_playlist:
                    if verificarMusicaPlaylist(uri_playlist, uri_musica, nome_musica) == True:
                        abrir_spotify()
                        id_dispositivo = dispositivos_conectados()
                        if tocarMusicaPlaylist(uri_playlist, uri_musica, id_dispositivo):
                            maquina.say('Tocando música')
                            maquina.runAndWait()
            #Reproduz a playlist desejada
            elif 'playlist' in musica:
                palavra_chave1 = 'playlist'
                nome_playlist = descobreNome(palavra_chave1, musica)
                if nome_playlist:  
                    uri_playlist = obter_uri_playlist(nome_playlist)
                    print(f"A uri da playlist {nome_playlist} é: {uri_playlist}")
                    if uri_playlist:
                        abrir_spotify()
                        id_dispositivo = dispositivos_conectados()
                        sp.start_playback(device_id=id_dispositivo, context_uri=uri_playlist)
                        maquina.say('Tocando música')
                        maquina.runAndWait()
                        print(f"Tocando Playlist: {nome_playlist}")
            #Reproduz a música desejada
            else:
                palavra_chave1 = 'toque'
                nome_musica = descobrePalavras(palavra_chave1, comando)
                uri_musica = obter_uri_musica(nome_musica)
                print(f"Sua música é: {nome_musica} com URI: {uri_musica}")
                if uri_musica:
                    abrir_spotify()
                    id_dispositivo = dispositivos_conectados()
                    sp.start_playback(device_id=id_dispositivo, uris=[uri_musica])
                    maquina.say('Tocando música')
                    maquina.runAndWait()
                    print(f"Tocando música: {nome_musica}")
    except Exception as e:
        print(f"Erro na execução da função 'comando_voz_usuario': {e}")
        maquina.say("Erro na execução da função")
        maquina.runAndWait()
    print("-="*30)
    #"""

#Ativa o picovoice pra capturar o áudio do microfone
def main():
    try:
        ativada = picovoice()
        if ativada:#Se for capturada a palavra "Joana" no microfone, ele executa a função para capturar o comando
            comando_voz_usuario()
        else:
            time.sleep(1) 
    except Exception as e:
        print(f"Ocorreu um erro: {e}. Reiniciando a aplicação...")
        time.sleep(2)  # Espera antes de reiniciar 

if __name__ == "__main__":
    while True:
        main()
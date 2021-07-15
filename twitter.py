#Criado por: Fernando Groders
#Linguagem: Python 3.8.7
#Data da última atualização: 13/07/2021

from datetime import datetime
import tweepy
import requests
import time
import os
from os import environ
from random import randint
from data import db

# API_KEY = environ['API_KEY'] #Autenticadores do Twitter
# API_KEY_SECRET = environ['API_KEY_SECRET'] #Variáveis setadas no Heroku
# ACCESS_TOKEN = environ['ACCESS_TOKEN']
# ACCESS_SECRET = environ['ACCESS_SECRET']
# API_KEY_TMDB = environ['API_KEY_TMDB']

API_KEY = 'bowoyP9rnFeXiKjsRCwqhXLmG'
API_KEY_SECRET = 'sYeU8Lisr5qk3mI4A74RWMPQSNBtX1QEwWOKunBGflnX4rLXUq'
ACCESS_TOKEN = '1414621937402322952-6dw9hiLbMKCIAOC5lkBRhZLGpKOHr3'
ACCESS_SECRET = 'm9dTAnWHMGJKsDOdN6K2HG0T0fnkToA6JfohwE1z0MUWq'
API_KEY_TMDB = 'eaa42507ce91f5145d52e2006ab0725a'


auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
database = db
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) #Autentica a conta

def sorteiaPagina():
    numeroPagina = randint(0,140)
    return numeroPagina

def sorteiaFilme():
    numeroFilme = randint(0,9)
    return numeroFilme

def le_ultimo_id_lido(): #Função que lê o ultimo id lido pelo bot que fica salvo em um .txt separado
    return database.getUltimoIdLido()

def guarda_ultimo_id_lido(ultimo_id_lido): #Função que salva o ultimo id lido pelo bot
    database.updateUltimoIdLido(ultimo_id_lido)

def requestListaFilmes():
    print('--------------------------------') 
    pagina = str(sorteiaPagina())
    link = 'https://api.themoviedb.org/3/discover/movie?with_watch_providers=8&watch_region=BR&page={0}&api_key={1}&language=pt-BR'.format(pagina,API_KEY_TMDB)
    response = requests.get(link)
    responseJson = response.json()["results"]
    responseFinal = responseJson[sorteiaFilme()]
    id = responseFinal["id"]
    return id

def requestFilmeEspecifico():
    id = requestListaFilmes()
    link = 'https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=pt-BR'.format(id,API_KEY_TMDB)
    response = requests.get(link)
    responseFinal = response.json()
    return responseFinal

def tweet_image(url, message, mention):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message, in_reply_to_status_id=mention)
        os.remove(filename)
    else:
        print("Não foi possível baixar a imagem!")

def fazerTweet():
    print(formatarHoras(),'BOT TRABALHANDO...')
    ultimo_id_lido = le_ultimo_id_lido()
    mentions = api.mentions_timeline(ultimo_id_lido , tweet_mode='extended') #Lê as menções ao bot e salva em um vetor
    for mention in reversed(mentions): #'reserved(mentions)' serve para ler o vetor do mais velho para o mais novo
        if '@dizumfilme' in mention.full_text.lower(): #Verificação apenas para garantir que o bot vai ler todas menções, independente de letra maiúscula ou minúscula
            jsonFilme = requestFilmeEspecifico()
            print(str(mention.id) + ' - ' + mention.full_text)
            ultimo_id_lido = mention.id
            guarda_ultimo_id_lido(ultimo_id_lido) #Salva o id lido
            print('Respondendo tweet')
            
            anoLancamento = jsonFilme["release_date"]
            fraseFormatada = 'Olá @{}! 🎥 Minha indicação para você é: {} | 🎞️ Gênero: {} | ⭐ Nota: {}/10.0 | 🎉 Ano de lançamento: {} | 🔎 Ver mais sobre: https://www.imdb.com/title/{}' #Formata a frase       
            fraseFormatada = fraseFormatada.format(mention.user.screen_name, jsonFilme["title"], jsonFilme["genres"][0]['name'], str(jsonFilme["vote_average"]), str(anoLancamento[0:4]), str(jsonFilme["imdb_id"]))
            
            linkImagem = 'https://image.tmdb.org/t/p/w500{}'.format(jsonFilme['poster_path'])           
            
            tweet_image(linkImagem, fraseFormatada, mention.id)

def formatarHoras():
    now = datetime.now()
    horas = '[{}:{}:{}]'.format(now.hour,now.minute,now.second)
    return horas

while True: #Loop que a atualiza o bot a cada 60 segundos
    fazerTweet()  
    time.sleep(60)
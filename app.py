import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import urllib.request

urlcekongkir = "https://pluginongkoskirim.com/cek-tarif-ongkir/front/resi-amp?__amp_source_origin=https%3A%2F%2Fpluginongkoskirim.com"
urlyoutube = "http://sosmeeed.herokuapp.com:80/api/youtube/video"
urltwitter = "http://sosmeeed.herokuapp.com:80/api/twitter/video"


bot = telebot.TeleBot("717811256:AAFpTRD8AZ90t6nqpayMvL5fpxG7ElFBf9c")
tb = telebot.TeleBot("717811256:AAFpTRD8AZ90t6nqpayMvL5fpxG7ElFBf9c")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Golek opo Su?")


""" ================================================================================================== """
@bot.message_handler(commands=['cekresi'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('jnt', 'jne')
    sent = bot.send_message(message.chat.id, 'Pilih Kurir', reply_markup=keyboard)
    bot.register_next_step_handler(sent, resi)

def resi(message):
    global kurir
    kurir = (message.text)
    sent2 = bot.send_message(message.chat.id, 'Input Resi')
    bot.register_next_step_handler(sent2, botstarted)

def botstarted(message):
    resi = (message.text)
    
    payload={'kurir': kurir,'resi': resi}
    files=[]
    response = requests.request("POST", urlcekongkir, data=payload, files=files)
    datakurir = response.json()
      
    resi_kurir = datakurir['data']['detail']['code']
    status_kurir = datakurir['data']['detail']['status']
    lokasi_terakhir = datakurir['data']['detail']['history'][0]['position']
    desc_terakhir = datakurir['data']['detail']['history'][0]['desc']
    
    bot.reply_to(message, "RESI : " + resi_kurir + "\nSTATUS : " + status_kurir + "\n===========================" "\nLokasi : " + lokasi_terakhir + "\nDESC : " + desc_terakhir)
""" ================================================================================================== """
@bot.message_handler(commands=['twitter'])
def starttwiter(message):
    global tiktokurl
    sent2 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent2, twitterstarted)

def twitterstarted(message):
    twitterurl = (message.text)
    
    payloadtwitter='url='+twitterurl
    headerstwitter = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    responsetwitter = requests.request("POST", urltwitter, headers=headerstwitter, data=payloadtwitter)

    datatwitter = responsetwitter.json()
      
    vide_urltwt = datatwitter['data']['data'][0]['link']
    bot.send_video(message.chat.id,vide_urltwt)



bot.polling()

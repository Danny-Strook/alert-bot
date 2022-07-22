import requests
import json
import telebot
import time
import config

bot = telebot.TeleBot(config.bottocken)

maxprice = 24500
minprice = 18500


def alert_check(price):   # alert function
    global maxprice
    global minprice
    if price > maxprice:
        bot.send_message(492639112, 'BTC above alert line!')
        maxprice += 500
    elif price < minprice:
        bot.send_message(492639112, 'BTC below alert line!')
        minprice -= 500


def getprice_bin(coin1="btc", coin2="usdt"):
    url = 'https://fapi.binance.com/fapi/v1/ticker/price'
    param = {'symbol': f'{coin1.upper()}{coin2.upper()}'}
    response = requests.get(url, params=param)
    price = float(response.json()['price'])
    return price


def main():
    while True:
        alert_check(getprice_bin())
        time.sleep(10)


if __name__ == '__main__':
    main()

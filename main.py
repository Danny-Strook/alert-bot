import requests
import time
import config

bot_token=config.bot
chat_id='492639112'

above=16500
below=15950


telegram_delay=10
def getTPSLfrom_telegram():
    global above, below
    strr='https://api.telegram.org/bot'+bot_token+'/getUpdates'
    response = requests.get(strr)
    rs=response.json()
    rs2=rs['result'][-1]
    rs3=rs2['message']
    msg_cont=rs3['text']
    datet=rs3['date']

    if(time.time()-datet)<telegram_delay:
        if 'Above' in msg_cont:
            above=int(msg_cont[5:])
            telegram_bot_sendtext(str(above))
        if 'Below' in msg_cont:
            below=int(msg_cont[5:])
            telegram_bot_sendtext(str(below))
        if 'Spread' in msg_cont:
            msgt=str(below)+' : '+str(above)
            telegram_bot_sendtext(msgt)
        

def telegram_bot_sendtext(bot_message):
    bot_token2 = bot_token
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token2 + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

class Price:    # the class recieves pair name and link for api requests to return price using certain method
    def __init__(self, pair, source):
        self.pair = pair
        self.source = source

# get a price from binance
    def getprice_bin(self):
        url = self.source
        param = {'symbol': self.pair}
        r = requests.get(url, params=param)
        if r.status_code == 200:
            data = r.json()
        else:
            print('error')
            # bpbtc = b -binance + p-price + btc - ticker
        price = float(data['price'])
        return price

bbtc = Price('BTCUSDT', 'https://fapi.binance.com/fapi/v1/ticker/price')


def alert_check(price):   # alert function
    global above,below
    if price > above:
        msg='Above alert line!'
        above+=100
        telegram_bot_sendtext(msg)
    elif price < below:
        msg='Below alert line!'
        below-=100
        telegram_bot_sendtext(msg)


def main():
    while True:
        getTPSLfrom_telegram()
        alert_check(bbtc.getprice_bin())
        time.sleep(10)


if __name__ == '__main__':
    main()

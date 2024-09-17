import time
from datetime import datetime

from config import API_KEY, API_SECRET, ACCOUNT, SYMBOL, DATE_LISTING
from pybit.unified_trading import HTTP

client = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET
)

symbol_without_usdt = SYMBOL.replace("USDT", "")
available_balance = "" 

def get_balance():
    global available_balance
    try:
        balance = client.get_wallet_balance(accountType=ACCOUNT)
        
        if balance['retCode'] == 0:
            balances = balance['result']['list'][0]['coin']
            
            for coin_info in balances:
                if coin_info['coin'] == symbol_without_usdt:
                    coin = coin_info['coin']
                    available_balance = coin_info.get('walletBalance', 0)
                    print(f"Coin: {coin}, Available Balance: {available_balance}")
                    break  
        else:
            print(f"Errore dalla API: {balance['retMsg']}")
    except Exception as e:
        print(f"Errore durante il recupero del bilancio: {e}")

def sell_dogs():
    try:
        # Ordine di mercato
        order = client.place_order(
            category="spot",  # spot
            symbol=SYMBOL,
            side="Sell",
            orderType="Market",
            qty=available_balance
        )
        print(f"Ordine di vendita inviato: {order}")
    except Exception as e:
        print(f"Errore durante l'invio dell'ordine di vendita: {e}")

def check_and_sell():
    now = datetime.now()
    target_time = DATE_LISTING

    # Calcola il tempo rimanente fino al target_time
    time_remaining = target_time - now

    # Stampa data e ora correnti e il tempo rimanente
    print(f"Ora attuale: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Tempo rimanente fino al target: {str(time_remaining)}")

    if now >= target_time:
        print(f"È il momento di vendere i {symbol_without_usdt}")
        get_balance()
        sell_dogs()
    else:
        print(f"Non è ancora il momento di vendere {symbol_without_usdt}. Attendi fino a {target_time}.")
        time.sleep(60)  # Attendere un minuto prima di riprovare

if __name__ == "__main__":
    check_and_sell()

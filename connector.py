from config import API_KEY, API_SECRET, ACCOUNT, SYMBOL
from pybit.unified_trading import HTTP

client = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

symbol_without_usdt = SYMBOL.replace("USDT", "")
available_balance = "" 

def getBalance():
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
            print(f"Error API: {balance['retMsg']}")
    except Exception as e:
        print(f"Error get balance: {e}")

def sellCoins():
    try:
        # Ordine di mercato
        order = client.place_order(
            category="spot",  # spot
            symbol=SYMBOL,
            side="Sell",
            orderType="Market",
            recv_window=6000,
            qty=available_balance,
            max_retrives=5
        )
        print(f"Ordine di vendita inviato: {order}")
    except Exception as e:
        print(f"Errore durante l'invio dell'ordine di vendita: {e}")

def checkAndSell():

    getBalance()
    sellCoins()
   

if __name__ == "__main__":
    checkAndSell()

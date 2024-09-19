import time
import logging
from datetime import datetime
from config import API_KEY, API_SECRET, ACCOUNT, SYMBOL, LISTING_DATE
from pybit.unified_trading import HTTP

# Set up logging
logging.basicConfig(
    filename="sell_log.log", 
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"  
)

# Convert LISTING_DATE string to a datetime object
listing_date_obj = datetime.strptime(LISTING_DATE, "%d/%m/%Y %H:%M")

client = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

symbol_without_usdt = SYMBOL.replace("USDT", "")
available_balance = 0.0 

def getBalance():
    global available_balance
    try:
        balance = client.get_wallet_balance(accountType=ACCOUNT)
        
        if balance['retCode'] == 0:
            balances = balance['result']['list'][0]['coin']
            
            for coin_info in balances:
                if coin_info['coin'] == symbol_without_usdt:
                    coin = coin_info['coin']
                    available_balance = float(coin_info.get('walletBalance', 0))  # Convert to float
                    logging.info(f"Coin: {coin}, Available Balance: {available_balance}")
                    print(f"Coin: {coin}, Available Balance: {available_balance}")
                    break  
        else:
            logging.error(f"API Error: {balance['retMsg']}")
            print(f"API Error: {balance['retMsg']}")
    except Exception as e:
        logging.error(f"Error getting balance: {e}")
        print(f"Error getting balance: {e}")

def sellCoins():
    global available_balance
    if available_balance <= 0:
        logging.warning("Cannot sell, insufficient funds.")
        print("Cannot sell, insufficient funds.")
        return

    try:
        # Place a sell order
        order = client.place_order(
            category="spot",  # spot
            symbol=SYMBOL,
            side="Sell",
            orderType="Market",
            recv_window=6000,
            qty=available_balance,  # Use available balance
            max_retrives=5
        )
        logging.info(f"Sell order sent: {order}")
        print(f"Sell order sent: {order}")
    except Exception as e:
        logging.error(f"Error sending sell order: {e}")
        print(f"Error sending sell order: {e}")

def checkAndSell():
    getBalance()
    sellCoins()

def checkAndSellAtScheduledTime():
    while True:
        current_time = datetime.now()

        if current_time >= listing_date_obj:
            logging.info(f"Sale time has arrived. Current time: {current_time}. Starting sell process.")
            checkAndSell()
            break 

        time_diff = listing_date_obj - current_time
        hours_left, remainder = divmod(time_diff.seconds, 3600)
        minutes_left, seconds_left = divmod(remainder, 60)

        print(f"Time left until sale: {hours_left} hours, {minutes_left} minutes, {seconds_left} seconds.")
        
        time.sleep(1)

if __name__ == "__main__":
    logging.info("Crypto sell script started.")
    checkAndSellAtScheduledTime()

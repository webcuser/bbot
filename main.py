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

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        try:
            # Place a sell order
            order = client.place_order(
                category="spot",
                symbol=SYMBOL,
                side="Sell",
                orderType="Market",
                recvWindow=6000,
                qty=str(available_balance)
            )
            if order.get('retCode') == 0:
                logging.info(f"Sell order successful on attempt {attempt}: {order}")
                print(f"Sell order successful on attempt {attempt}: {order}")
                return
            else:
                logging.error(f"API Error on attempt {attempt}: {order.get('retMsg')}")
                print(f"API Error on attempt {attempt}: {order.get('retMsg')}")
        except Exception as e:
            logging.error(f"Error sending sell order on attempt {attempt}: {e}")
            print(f"Error sending sell order on attempt {attempt}: {e}")

        if attempt < max_attempts:
            time.sleep(0.5)

    logging.error("Failed to sell coins after all attempts.")
    print("Failed to sell coins after all attempts.")

def checkAndSell():
    # Retry getting balance as it might take a few seconds to appear after listing
    max_balance_attempts = 5
    for attempt in range(1, max_balance_attempts + 1):
        getBalance()
        if available_balance > 0:
            break
        if attempt < max_balance_attempts:
            logging.info(f"Balance is 0, retrying in 1s... (Attempt {attempt}/{max_balance_attempts})")
            print(f"Balance is 0, retrying in 1s... (Attempt {attempt}/{max_balance_attempts})")
            time.sleep(1)

    sellCoins()

def checkAndSellAtScheduledTime():
    while True:
        current_time = datetime.now()

        if current_time >= listing_date_obj:
            logging.info(f"Sale time has arrived. Current time: {current_time}. Starting sell process.")
            checkAndSell()
            break

        time_diff = listing_date_obj - current_time
        total_seconds = int(time_diff.total_seconds())
        hours_left, remainder = divmod(total_seconds, 3600)
        minutes_left, seconds_left = divmod(remainder, 60)

        print(f"\rTime left until sale: {hours_left} hours, {minutes_left} minutes, {seconds_left} seconds.", end="")

        time.sleep(1)

if __name__ == "__main__":
    logging.info("Crypto sell script started.")
    checkAndSellAtScheduledTime()

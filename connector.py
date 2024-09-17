from pybit import HTTP
from datetime import datetime, timedelta
import time

# Ваши API-ключ и секрет от Bybit
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Подключение к Bybit API
client = HTTP("https://api.bybit.com", api_key=API_KEY, api_secret=API_SECRET)
# Подключение к Testnet API Bybit
""" client = HTTP("https://api-testnet.bybit.com", api_key=API_KEY, api_secret=API_SECRET) """

# Функция для продажи всех монет
def sell_all_assets():
    # Получаем баланс пользователя
    balance = client.get_wallet_balance()["result"]
    
    # Пример для продажи всех доступных USDT
    symbol = "HMSTRUSDT"  # Валютная пара, которую вы хотите продать
    side = "Sell"       # Сторона сделки - продажа
    qty = balance["USDT"]["available_balance"]  # Продать весь баланс USDT
    
    # Оформляем рыночный ордер на продажу
    order = client.place_active_order(
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=qty,
        time_in_force="GoodTillCancel"
    )
    print(f"Продано {qty} {symbol}")

# Функция для ожидания времени
def wait_until_14():
    target_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    if datetime.now() > target_time:
        target_time += timedelta(days=1)
    
    wait_time = (target_time - datetime.now()).total_seconds()
    time.sleep(wait_time)

# Основная логика
if __name__ == "__main__":
    print("Ждем 14:00 для продажи всех монет...")
    wait_until_14()
    sell_all_assets()

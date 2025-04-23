import time
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from SmartApi import SmartConnect
from config import API_KEY, CLIENT_ID, CLIENT_SECRET, PASSWORD, TOTP_SECRET

NIFTY_200 = ["RELIANCE", "HDFCBANK", "INFY", "TCS", "ICICIBANK"]
trades_done = 0

def login():
    obj = SmartConnect(api_key=API_KEY)
    data = obj.generateSession(CLIENT_ID, PASSWORD, TOTP_SECRET)
    print("Logged in successfully.")
    return obj

def is_HHHL(stock):
    return True  # Replace with actual logic

def place_order(obj, symbol):
    global trades_done
    if trades_done >= 2:
        print("Max trades done for today.")
        return
    order = obj.placeOrder(
        variety="NORMAL",
        tradingsymbol=symbol,
        symboltoken="3045",  # Replace with correct token
        transactiontype="BUY",
        exchange="NSE",
        ordertype="MARKET",
        producttype="INTRADAY",
        duration="DAY",
        quantity=1
    )
    print(f"Trade Placed for {symbol}: {order}")
    trades_done += 1

def scan_and_trade():
    print(f"Running scan at {datetime.now().strftime('%H:%M:%S')}")
    obj = login()
    for stock in NIFTY_200:
        if is_HHHL(stock):
            place_order(obj, stock)
            if trades_done >= 2:
                break

scheduler = BackgroundScheduler()
scheduler.add_job(scan_and_trade, 'cron', hour=9, minute=15)
scheduler.start()

print("Auto-trading app is running...")
while True:
    time.sleep(60)

import os
import csv
import time

def log_trade(trade_type, price, amount):
    file_path = "trade_log.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["type", "price", "amount"])
        writer.writerow([trade_type, price, amount])

def main():
    print("NitroBot running in DEMO mode...")
    for i in range(3):
        log_trade("BUY", 63000 + i * 10, 0.0005)
        time.sleep(2)

if __name__ == "__main__":
    main()

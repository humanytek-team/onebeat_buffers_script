#!/bin/python3
import sys
import csv

# MTSKUS
# 0  - Stock Location Name
# 1  - Origin SL
# 2  - SKU Name
# 3  - SKU Description
# 4  - Buffer Size
# 5  - Replenishment Time
# 6  - Inventory at Site
# 7  - Inventory at Transit
# 8  - Inventory at Production
# 9  - Precio unitario
# 10 - TVC
# 11 - Throughput
# 12 - Unidad de Medida
# 13 - Reported Year
# 14 - Reported Month
# 15 - Reported Day

# Transactions
# 0  - Origin
# 1  - SKU Name
# 2  - Destination
# 3  - Transaction Type (in/out)
# 4  - Quantity
# 5  - Shipping Year
# 6  - Shipping Month
# 7  - Shipping Day


def main():
    skus_path = sys.argv[1]
    data_path = sys.argv[2]
    skus = load_skus(skus_path)
    load_data(skus, data_path)
    order_transactions(skus)
    greatest = get_greatest(skus)
    show(greatest)
    return greatest


def load_skus(path: str):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        skus = {r[2]: {
            'window': int(float(r[5])),
            'transactions': [],
        } for r in reader}
        return skus


def load_data(skus: dict, path: str):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for r in reader:
            if r[3] == 'OUT':
                try:
                    skus[r[1]]['transactions'].append((f'{r[5]}-{r[6]}-{r[7]}', float(r[4])))
                except:
                    pass


def order_transactions(skus: dict) -> None:
    for v in skus.values():
        v['transactions'].sort()


def get_greatest(skus: dict) -> list:
    return [
        (sku, get_greatest_by_sku(v['transactions'], v['window']))
        for sku, v in skus.items()
    ]


def get_greatest_by_sku(transactions: list, window: int) -> float:
    s = 0
    greatest = 0
    for i in range(len(transactions)):
        if i >= window:
            s -= transactions[i - window][1]
        s += transactions[i][1]
        greatest = max(s, greatest)
    return greatest


def show(greatest: list) -> None:
    for r in greatest:
        print(f'{r[0]},{r[1]}')


if __name__ == '__main__':
    main()

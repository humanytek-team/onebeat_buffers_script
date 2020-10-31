#!/bin/python3
import sys
import csv
from datetime import datetime, timedelta

ISO_DATE = '%Y-%m-%d'

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
    data_path = sys.argv[1]
    header, data = load_data(data_path)
    sort_data(data)
    generate_missing(data)
    sort_data(data)
    write_data(f'{data_path}_w.csv', header, data)
    return


def load_data(path: str) -> tuple:
    print('Loading data')
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)
        return (header, list(reader))


def write_data(path: str, header: list, data: list) -> None:
    print('Writing')
    with open(path, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)


def sort_data(data: list):
    print('Sorting data')
    data.sort(key=lambda r: (
        r[0],
        r[1],
        r[2],
        r[3],
        r[5],
        r[6],
        r[7],
    ))


def date_from_list(ts: list) -> datetime:
    return datetime.strptime('-'.join(ts), ISO_DATE)


def list_from_date(date: datetime) -> list:
    return date.strftime(ISO_DATE).split('-')


def generate_missing(data: list) -> None:
    print('Generating missings')
    data_filtered = [r for r in data if r[3] == 'OUT']
    prev = data_filtered[0]
    for r in data_filtered:
        if prev[:4] != r[:4]:
            prev = r
            continue
        s = date_from_list(prev[5:]) + timedelta(days=1)
        e = date_from_list(r[5:])
        for d in daterange(s, e):
            data.append([r[0], r[1], r[2], r[3], 0, *list_from_date(d)])
        prev = r


def daterange(start_date: datetime, end_date: datetime) -> datetime:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == '__main__':
    main()

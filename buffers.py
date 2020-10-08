#!/bin/python
import sys
import csv


def main():
    data_path = sys.argv[1]
    sku = sys.argv[2]
    replenishment_time_days = int(float(sys.argv[3]))
    data = load_data(data_path, {
        'SKU Name': sku,
        'Transaction Type (in/out)': 'OUT',
    })
    greatest = get_greatest(data, replenishment_time_days)
    print(greatest)
    return greatest


def load_data(path: str, filter_dict: dict = {}) -> list:
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)
        filter_list = [filter_dict.get(h, None) for h in header]

        def filter_function(row: []) -> bool:
            for t in zip(filter_list, row):
                if t[0] != None and t[0] != t[1]:
                    break
            else:
                return True
            return False

        data = filter(filter_function, reader)
        clean_data = map(lambda r: [f'{r[5]}-{r[6]}-{r[7]}', int(float(r[4]))], data)
        sorted_data = sorted(clean_data)
        pure_data = map(lambda r: r[1], sorted_data)
        return list(pure_data)


def get_greatest(data: [], window: int) -> int:
    sum = 0
    greatest = 0
    for i in range(len(data)):
        if i >= window:
            sum -= data[i - window]
        sum += data[i]
        greatest = max(sum, greatest)
    return greatest


if __name__ == '__main__':
    main()

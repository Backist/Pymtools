from csv import *
from json import *

def export_to_csv(data, path):
    with open(path, 'w') as csvfile:
        writer = writer(csvfile)
        writer.writerow(data)

def export_to_json(data, path):
    with open(path, 'w') as jsonfile:
        dump(data, jsonfile)

if __name__ == "__main__":
    ...

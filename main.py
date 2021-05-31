# This is a sample Python script.
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    headerList = ["i", "brain", "body"]
    data = pd.read_fwf("/home/pau/PycharmProjects/ufz/mlPy/data/brainbodyratio.txt")
    for col in data.columns:
        print(col)

    res = stats.linregress(data['brain'], data['body'])
    print(res)
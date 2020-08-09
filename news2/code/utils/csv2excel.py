import pandas as pd

data = pd.read_json("/home/congw/PycharmProjects/untitled/data_Huffpost_U.S.-China trade and COVID-19.json")
data.to_excel("text.xlsx")
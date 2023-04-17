import pandas as pd

# aliments

# df = pd.read_excel("C:/Users/81317/OneDrive/桌面/Aliments.xlsx", index_col=0)
#
# print(df[:100])
#
# df.to_csv("C:/Users/81317/OneDrive/桌面/Aliments.csv", sep=';')


df = pd.read_csv("C:/Users/81317/OneDrive/桌面/Contenir.csv", dtype={'CodeA': int, 'CodeM': int}, index_col=0)

df.to_csv("C:/Users/81317/OneDrive/桌面/Contenir1.csv")

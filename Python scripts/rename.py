import pandas as pd


rename_path = 'D:\\data\\rename.xlsx'
path = 'D:\\data\\'
file = 'AgentReady.xlsx'
sheet = 'Sheet1'
column_index = 2

df1 = pd.read_excel(rename_path, sheet_name='test')

dict = dict(zip(df1.iloc[:, 0], df1.iloc[:, 1]))


df = pd.read_excel(path + file, sheet_name=sheet)

df.iloc[:, column_index] = df.iloc[:, column_index].replace(dict)

df.to_excel(path + "update_" + file, sheet_name=sheet, index=False)
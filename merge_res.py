import pandas as pd
import numpy as np

xls = pd.ExcelFile('merged_issues.xls')
df1 = pd.read_excel(xls, 'practo')
df2 = pd.read_excel(xls, 'zocdoc')


df=df1.append(df2, ignore_index=True)

print(df.head())

df.to_csv("xxx.csv",index=False)
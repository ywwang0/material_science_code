import pandas as pd
import re

df = pd.read_excel('binary.xlsx')
for n,i in enumerate(list(df['Formula'])):
    # 判断化学式中有没有数字
    if len(re.findall(r"\d+\.?\d*",i)) == 0:
        df.loc[n,'if natoms greater than 30'] = 0
    # 最大的数字小于30就是没超过30
    elif eval(max(re.findall(r"\d+\.?\d*",i))) < 30:
        df.loc[n,'if natoms greater than 30'] = 0
    else:
        df.loc[n,'if natoms greater than 30'] = 1
df.to_csv('out.csv',index=False)

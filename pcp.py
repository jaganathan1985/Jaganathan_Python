import pandas as pd
import json
from pandas.io.json import json_normalize

sodp = pd.read_csv('Input_StartOfDay_Positions.txt')
df_sodp = sodp.copy()
df_sodp['Delta']=0
sodp.fillna(-99999,inplace=True)
with open('1537277231233_Input_Transactions.txt') as f:
          jsondata=json.load(f)
df_transdata = pd.DataFrame.from_dict(json_normalize(jsondata),orient='columns')

x = 0
while x < len(df_transdata):
    y = 0
    while y < len(df_sodp):
        if(df_sodp['Instrument'].loc[y]==df_transdata['Instrument'].loc[x]):
            if((df_sodp['AccountType'].loc[y]=='E') and (df_transdata['TransactionType'].loc[x]=='B')):
                df_sodp['Quantity'].loc[y]= df_sodp['Quantity'].loc[y] + df_transdata['TransactionQuantity'].loc[x]
                df_sodp['Delta'].loc[y]= df_sodp['Quantity'].loc[y] - sodp['Quantity'].loc[y]
            

            if((df_sodp['AccountType'].loc[y]=='I') and (df_transdata['TransactionType'].loc[x]=='B')):
                tempval=sodp['Quantity'].loc[y]
                df_sodp['Quantity'].loc[y]= df_sodp['Quantity'].loc[y] - df_transdata['TransactionQuantity'].loc[x]
                df_sodp['Delta'].loc[y]= df_sodp['Quantity'].loc[y] - sodp['Quantity'].loc[y]

            if((df_sodp['AccountType'].loc[y]=='E') and (df_transdata['TransactionType'].loc[x]=='S')):
                df_sodp['Quantity'].loc[y]=df_sodp['Quantity'].loc[y] - df_transdata['TransactionQuantity'].loc[x]
                df_sodp['Delta'].loc[y]= df_sodp['Quantity'].loc[y] - sodp['Quantity'].loc[y]

            if((df_sodp['AccountType'].loc[y]=='I') and (df_transdata['TransactionType'].loc[x]=='S')):
                df_sodp['Quantity'].loc[y]=df_sodp['Quantity'].loc[y] + df_transdata['TransactionQuantity'].loc[x]
                df_sodp['Delta'].loc[y]= df_sodp['Quantity'].loc[y] - sodp['Quantity'].loc[y]
                
        y = y + 1
    x = x + 1
print(df_sodp)
        

#%%
from matplotlib.pyplot import axis
from sqlalchemy import true
import DBconnection as DB
import pandas as pd
import datetime as dt 

eng = DB.get_engine() 


def ELT_table(table_name,url, df):
    df['current_flag'] = 1 
    df['source'] = 'ABARES'
    df['source_link'] = url
    df['insert_date'] = dt.date.today()
    df['expiry_date'] = dt.date.max
    df.to_sql(table_name,eng,index=True,if_exists='replace', schema='raw')

# %%

# %%
table_name_prod ='abare_historical_productivity'
link_prod = 'https://www.awe.gov.au/sites/default/files/documents/fdp-beta-productivity-estimates.xlsx'
# get TFP data 
sheets =  {'Table 18':'Beef',
'Table 19':'Sheep',
"Table 20":"Mixed",
"Table 21":"Cropping",
"Table 22":"All industies",
"Table 52":"Dairy"
}

df = pd.DataFrame()
for key,item in sheets.items():
    df2 = pd.read_excel(link_prod, sheet_name=key,header=8)
    df2.columns = ['year', 'input', 'output', 'tfp']
    df2['state'] ='New South Wales'
    df2['industry'] = item
    df2 =  df2[df2['year'].str.startswith('2','1')==True]
    df = df.append(df2)
    print(df.head()) 


ELT_table(table_name_prod,link_prod, df)

# %%

# get state data 
table_name_state ='abare_historical_state_estimates'
link_state = 'https://www.awe.gov.au/sites/default/files/documents/fdp-beta-state-historical.csv'
df = pd.read_csv(link_state)
ELT_table(table_name_state,link_state, df)
# %%

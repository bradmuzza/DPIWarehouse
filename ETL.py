#%%
from requests import delete
import sqlalchemy 
import DBconnection as DB
import Datahelper
import pandas as pd
from sqlalchemy import insert, true
from sqlalchemy import delete
from sqlalchemy import update


#%%
eng = DB.get_engine() 
#%%
df = pd.read_excel(r"c:\Users\murrab01\OneDrive - DPIE\Documents\Data\Base Data Table ETL powerquerylist.xlsx")
#%%
df = df[df["Created"]<'2022-07-05']

#%%
df = df.rename(columns={"Targetdata": "TargetDate", "Enddate": "EndDate", "Measure": "Outcome", "Title": "Measure"})
df["IsCurrent"] = 1 
df["ExpiryDate"] = Datahelper.get_expiry_date()
df["InsertDate"]= Datahelper.get_insert_date()

df_2=df[['Id','Outcome', 'Modified','Created', 'Measure','SourceLink', 'Frequency', 'EndDate', 'Unit',
       'Baseline', 'StrategicPriority', 'Target', 'TargetDate' , "ExpiryDate","InsertDate","IsCurrent"]]
df_2
#%%
df_2.to_sql('BaseLineMeasures',eng,index=True,if_exists='replace', schema='raw')
#%%


df = pd.read_excel(r"c:\Users\murrab01\OneDrive - DPIE\Documents\Data\Monthly Data Table ETL powerquerylist.xlsx",
                  )
df = df[['Id','Title',
       'Modified', 'Created','Outcome',
       'StrategicPriority', 'Data', 'DateMeasured', 'MeaurementInterval',
       'ReportedCycleMMMYYYY', 'Status']]

df= df.rename(columns={"Title":"Measure","MeaurementInterval":"MeasurementInterval"})
df
#%%
table_name = "BaseLineMeasures"

def update_ELT_processing_Table(table_name,connect,is_insert=False):
    if true:
        connect.execute(F"""Update Raw.ETLUpdates
                        set  UpdateDate = '{Datahelper.get_insert_date()}'
                        where RefTable  = '{table_name}'
                        """)   
    if is_insert:
       connect.execute(f"""INSERT INTO Raw.ETLUpdates (RefTable)
                        VALUES ('{table_name}')
                        """) 
    

update_ELT_processing_Table(table_name,eng)


#%%

def get_ETL_table_process(con):
    return pd.read_sql("select * from raw.ETLUpdates", con)

def get_update_date_from_ETLUpdate(dataframe, table):
    return dataframe.query(f'RefTable == "{table}"')['UpdateDate'].values[0]

df= get_ETL_table_process(eng)
get_update_date_from_ETLUpdate(df,table_name)

# %%

df.query(f'RefTable == "BaseLineMeasures"')['UpdateDate'].values[0]

# %%

#%%
from ast import Str, excepthandler
import datetime
import calendar as cl

from pandas import concat
from sqlalchemy import except_all 


def clean_text(txt):
    txt = txt.str.replace("(<br/>)", "")
    txt = txt.str.replace('(<a).*(>).*(</a>)', '')
    txt = txt.str.replace('(&amp)', '')
    txt = txt.str.replace('(&gt)', '')
    txt = txt.str.replace('(&lt)', '')
    txt = txt.str.replace('(\xa0)', '')  
    return txt

def get_expiry_date():
    return datetime.datetime(9999,12,31)

def get_insert_date():
    return datetime.datetime.today()

def get_YYYYMM_from_string(text):
    month_string = text.split()[0] 
    month_string = month_string.capitalize()
    year  = text.split()[1] 
    try:
        month_number =  list(cl.month_abbr).index(month_string)
    except:
        month_number =  list(cl.month_name).index(month_string)
    combined =  year+str(month_number if month_number>9 else '0'+str(month_number))
    return combined 
   
        

#%%
# %%
  # def get_existing_baseline_data_from_DB(self):
    #     return pd.read_sql("select * from raw.BaseLineMeasures", self.con)

    # def update_ELT_processing_Table(self,is_new_table=False):
    #     if is_new_table!=True:
    #         sql_string = F"""Update Raw.ETLUpdates
    #                         set  UpdateDate = '{self.Insert_date}'
    #                         where RefTable  = '{self.table_name}'
    #                         """   
    #     if is_new_table:
    #         sql_string = f"""INSERT INTO Raw.ETLUpdates (RefTable)
    #                         VALUES ('{self.table_name}')
    #                         """
    #     self.sql_exectue(sql_string)
    
     # def get_ETL_table_process(self):
    #     return pd.read_sql("select * from raw.ETLUpdates", self.con)

    # def get_update_date_from_ETLUpdate(self):
    #     df = pd.read_sql(f"select * from raw.ETLUpdates where RefTable = '{self.table_name}' ", self.con)
    #     if len(df)>0:
    #         return df['UpdateDate'].values[0]
    #     else:
    #         return self.expiry_date
    
      # def get_modified_records(self,dataframe):
    #     last_updated = self.get_update_date_from_ETLUpdate()
    #     df_new_record = dataframe[dataframe["Modified"]>f"{last_updated}"]
    #     return df_new_record
    
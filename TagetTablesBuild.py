#%%
from enum import unique
from os import rename
from pip import main
from regex import I
from requests import delete
import sqlalchemy 
import DBconnection as DB
import Datahelper
import pandas as pd
from sqlalchemy import column, insert, true
from sqlalchemy import delete
from sqlalchemy import update


def create_target_forcast_data_frame(row,freq):
    if freq == "Y":
        freq = pd.DateOffset(years=1)
    if freq == "2Y":
        freq = pd.DateOffset(years=2)
    if freq =="6M":
        freq = pd.DateOffset(months=6)
             
    return pd.DataFrame({"StrategicPriority": row['StrategicPriority'].values[0],
              "Measure":row['Measure'].values[0], 
              "Peroids": row['PeriodsToTarget'].values[0],
              "Baseline": row['BaselineData'].values[0],
              "TargetDate":row["TargetDate"].values[0],
              "FK_measure": row["FK_Measure"].values[0],
              "Date":pd.date_range(row['BaseDate'].values[0],
                                   periods=row['PeriodsToTarget'].values[0]+1, 
                                   freq=freq),
              "FlatTarget": row['TargetData'].values[0],
              })
    
def sql_exectue(sql,con):
        with con.begin() as eng:
            eng.execute(sql)

def delete_existing_cycle_records(report_cycle, eng):
    sql = f"""
    delete from Staging.TargetForecasts
    where ReportCycle= '{report_cycle}'
    """
    sql_exectue(sql,eng)
    
    
            

def update_target_forecast(dataframe, report_cycle,forecastStartText):
    df =  dataframe.copy()
    for i in range(1,len(df)+1):
        df_row = df.iloc[i-1:i]
        freq = df_row['Frequency'].values[0]
        baseline = df_row["BaselineData"].values[0]
        target = df_row["TargetData"].values[0]
        if baseline is None or target is None:
            CGAR = 0 
            Marginal_growth = 0         
        elif baseline==0:
            CGAR = (target/(baseline+0.0001))**(1/df_row["PeriodsToTarget"].values[0])
            Marginal_growth = (target-baseline)/df_row["PeriodsToTarget"].values[0]
        else:
            CGAR = (target/baseline)**(1/df_row["PeriodsToTarget"].values[0])
            Marginal_growth = (target-baseline)/df_row["PeriodsToTarget"].values[0]
        
        if freq == "Quarterly":  
            df_target = create_target_forcast_data_frame(df_row,'Q') 

        elif freq== "Annually":
            df_target = create_target_forcast_data_frame(df_row,'Y') 
           
        elif freq== "Monthly":
            df_target = create_target_forcast_data_frame(df_row,'M') 
            
        elif freq == 'Biannual':
            df_target = create_target_forcast_data_frame(df_row,'6M') 
            
        elif freq == 'Biennial':
            df_target = create_target_forcast_data_frame(df_row,'2Y') 
           

        df_target["CompandGrowthTarget"] = [y*CGAR**x for x, y in df_target["Baseline"].iteritems() ]
        df_target["LinearGrowthTarget"]  = [y+(Marginal_growth*(x)) for x, y in df_target["Baseline"].iteritems() ]
        df_target["Frequency"] = freq
        df_target["ReportCycle"] = report_cycle
        df_target['ForecastStart'] = forecastStartText
        df_target["Target"] = target
        # change to if_Exist= "append"
        df_target.to_sql("TargetForecasts", con=eng, schema="Staging",if_exists="append")

# %%
if __name__ == "__main__":
    report_cycle = "202207"
    eng = DB.get_engine() 
    delete_existing_cycle_records(report_cycle,eng)
    Sql_last = "select * from [Staging].[TargetFirstBaselineView] where BaseDate is not null"
    df=pd.read_sql(sql=Sql_last,con=eng)
    update_target_forecast(df,report_cycle,'First BaseLine')
#%%  
if __name__ == "__main__":
    report_cycle = "202207"
    eng = DB.get_engine()  
    sql_first = "select * from Staging.TargetLastBaselineView "
    
    df=pd.read_sql(sql=sql_first,con=eng)
    update_target_forecast(df,report_cycle,'Historical')
    

# %%

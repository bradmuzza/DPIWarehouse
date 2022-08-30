import pandas as pd
from sqlalchemy import create_engine
import json 


with open("DB_settings.json") as j:
    config =  json.load(j)


def get_engine():
    url = f"mssql+pyodbc://{config['User']}:{config['Password']}@{config['Host']}:{config['Port']}/{config['DataBase']}?driver=SQL+Server"
    eng =create_engine(url)
    return eng









     
